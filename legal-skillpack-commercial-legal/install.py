#!/usr/bin/env python3
"""Standalone skill installer for the Legal Agent Skillpack portable release.

本文件被 ``src/export/build_release.py`` 复制到分发包根目录，命名为
``install.py``。它**不依赖本项目源码**，只用 Python 3.9+ 标准库。

host-agnostic 设计：从 ``EXPORT-MANIFEST.json`` 读 ``host_id``，按内置表查默认目标目录。
所有 host（codex / myagents / cursor / agents / opencode / kimi-code / openclaw / workbuddy）
都用同一个 installer。

用法：

    python3 install.py                # 自动检测平台并装到对应目录（多平台时交互选择）
    python3 install.py --target DIR   # 强制装到指定目录（覆盖自动检测）
    python3 install.py --host NAME    # 显式指定目标平台（codex/workbuddy/myagents/...）
    python3 install.py --force        # 覆盖同名 skill 目录（含非本包管理的目录，覆盖前自动备份）
    python3 install.py --uninstall    # 卸载本包管理的 skill
    python3 install.py --list         # 列出每个 skill 的安装状态
    python3 install.py --check-only   # 仅检测环境能力，不安装

自动检测规则：
- host_id == "portable" 时，扫描 ~/.claude / ~/.codex / ~/.workbuddy / ~/.kimi /
  ~/.config/opencode / ~/.openclaw / 当前目录的 .cursor，按检测结果选目录
- 检测到多个平台时：交互终端下由用户选择；非交互（脚本/CI）下拒绝静默猜测，
  要求显式传 --target 或 --host 后重试
- 未检测到任何平台时，回退到 ~/.agents/skills 并提示

不会调用网络、不会修改默认目标目录之外的位置、不会处理任何用户密钥。

Legal Gateway 状态：
- Legal Gateway（MCP 统一接入层）目前**尚未发布**（规划中）。
  `pip install legal-gateway` 当前不可用；文档中的 Gateway 说明仅描述目标设计。
- 含定时 Workflow 的 plugin，在 Gateway 发布前需手动触发（或在平台自身的
  定时任务能力中配置）；安装脚本会如实提示这一点。
- 详细兼容性检查见本目录 CHECKPOINT.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_ID = "claude-for-legal"
MARKER_FILE = ".legal-agent-skillpack-install.json"
# Legal Gateway 尚未发布（规划中）。下方文案仅用于如实提示状态，不要引导安装。
GATEWAY_STATUS_NOTE = (
    "Legal Gateway（MCP 统一接入层）尚未发布（规划中）。\n"
    "  发布前：`pip install legal-gateway` 不可用；定时 Workflow 需手动触发，\n"
    "  或在平台自身的定时任务能力（如 MyAgents Task、cron）中配置。"
)
PROFILE_HOME_VAR = "LEGAL_AGENT_PROFILE_HOME"
PROFILE_HOME_DEFAULT = "~/.legal-agent"

HERE = Path(__file__).resolve().parent
SKILLS_DIR = HERE / "skills"
WORKFLOWS_DIR = HERE / "workflows"
MANIFEST_PATH = HERE / "EXPORT-MANIFEST.json"

# host_id → 默认目标。新 host 在这里加一行，无需改其他代码。
# 注意：cursor 是相对当前 cwd 的 .cursor/skills（项目级），其他都是 ~/<dir>/skills 全局。
DEFAULT_TARGETS: dict[str, str] = {
    "codex": "~/.codex/skills",
    "workbuddy": "~/.workbuddy/skills",
    "opencode": "~/.config/opencode/skills",
    "openclaw": "~/.openclaw/skills",
    "kimi-code": "~/.kimi/skills",
    "myagents": "~/.claude/skills",
    "agents": "~/.agents/skills",
    "cursor": ".cursor/skills",
}
FALLBACK_TARGET = "~/.agents/skills"


@dataclass
class Summary:
    installed: int = 0
    updated: int = 0
    skipped: int = 0
    blocked: int = 0
    removed: int = 0
    details: list[str] = field(default_factory=list)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest() -> dict[str, Any]:
    if MANIFEST_PATH.exists():
        try:
            return _read_json(MANIFEST_PATH)
        except Exception:  # noqa: BLE001
            return {}
    return {}


def _resolve_host(manifest: dict[str, Any]) -> str:
    host = manifest.get("host_id") or "unknown"
    return host


def _resolve_default_target(host: str) -> Path:
    raw = DEFAULT_TARGETS.get(host, FALLBACK_TARGET)
    return Path(raw).expanduser().resolve()


def _normalize_target_path(raw: str | Path) -> Path:
    """规范化 --target / 回退目录，兼容 Git Bash (MSYS) 风格路径。

    Git Bash 会把 `/d/foo` 形式的参数原样传给 Python（不做盘符转换），
    而 Path.resolve() 会把 `/d/foo` 当作"当前盘符根目录下的 d 目录"，
    拼出错误落点。这里先做 MSYS 盘符映射，再展开 ~ 与环境变量。
    """
    s = os.path.expandvars(os.path.expanduser(str(raw))).strip()
    # MSYS 盘符映射：/d/foo → D:/foo（也兼容 /D/foo）
    m = re.fullmatch(r"/([A-Za-z])(/.*)?", s)
    if m and not s.startswith("//"):
        drive = m.group(1).upper()
        rest = m.group(2) or "/"
        s = f"{drive}:{rest}"
    return Path(os.path.normpath(s)).resolve()


def _pick_host_interactively(platforms: list[str]) -> str | None:
    """交互终端下让用户在多个检测到的平台中选择。非交互或选择失败返回 None。"""
    if not sys.stdin or not sys.stdin.isatty():
        return None
    print()
    print("检测到多个智能体平台。请选择本次安装目标（安装前请确认你在用哪个平台）：")
    for i, name in enumerate(platforms, 1):
        print(f"  {i}. {name} → {DEFAULT_TARGETS.get(name, FALLBACK_TARGET)}")
    print("  q. 退出，改用 --target <path> 或 --host <name> 指定")
    try:
        answer = input("输入编号后回车: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if answer.isdigit() and 1 <= int(answer) <= len(platforms):
        return platforms[int(answer) - 1]
    return None


def _resolve_target_for_install(host_id: str, host_override: str | None = None) -> Path:
    """决定安装目标目录。

    优先级：--host 显式指定 > manifest 的 host_id > 动态检测 > 通用回退目录。
    多平台并存时**不静默取第一个**：交互终端下由用户选择；非交互场景
    拒绝猜测，要求显式传 --target 或 --host 后重试（防止装进用不上的运行时）。
    """
    if host_override:
        if host_override not in DEFAULT_TARGETS:
            raise SystemExit(
                f"未知 host: {host_override}。可选值: {', '.join(DEFAULT_TARGETS)}"
            )
        print(f"已按 --host 指定平台: {host_override} → {DEFAULT_TARGETS[host_override]}")
        return _normalize_target_path(DEFAULT_TARGETS[host_override])

    if host_id in DEFAULT_TARGETS:
        return _normalize_target_path(DEFAULT_TARGETS[host_id])

    detected = _detect_platform()
    if detected == "unknown":
        print("⚠ 未检测到任何已知智能体平台。", file=sys.stderr)
        print(f"  默认装到通用目录: {FALLBACK_TARGET}", file=sys.stderr)
        print("  如需装到具体平台，请用: python3 install.py --target <path>", file=sys.stderr)
        return _normalize_target_path(FALLBACK_TARGET)

    platforms = detected.split(",")
    if len(platforms) > 1:
        chosen = _pick_host_interactively(platforms)
        if chosen is None:
            print(
                "⚠ 检测到多个平台且无法确认你在使用哪个。\n"
                "  为避免把 skill 装进用不上的运行时（装完看不见），本次不安装。\n"
                "  请显式指定后重试：\n"
                "    python3 install.py --host <平台名>   # 可选: "
                + ", ".join(platforms) + "\n"
                "    python3 install.py --target <目录>"
            )
            raise SystemExit(2)
    else:
        chosen = platforms[0]
        print(f"检测到平台: {chosen} → {DEFAULT_TARGETS.get(chosen, FALLBACK_TARGET)}")
    return _normalize_target_path(DEFAULT_TARGETS.get(chosen, FALLBACK_TARGET))


def _runtime_read_dir(host_id: str, host_override: str | None = None) -> Path | None:
    """返回目标平台运行时**实际读取** skill 的目录，用于安装后核对。

    只依据显式信息（--host 或 manifest host_id）判断；portable / unknown 时
    返回 None——绝不"猜第一个"，避免安装目录与运行时目录恰好同源而漏报警告。
    """
    explicit = host_override or (host_id if host_id in DEFAULT_TARGETS else None)
    if explicit is None:
        return None
    return _normalize_target_path(DEFAULT_TARGETS.get(explicit, FALLBACK_TARGET))


def _list_bundled_skills() -> list[Path]:
    if not SKILLS_DIR.exists():
        raise SystemExit(
            f"bundled skills dir not found: {SKILLS_DIR}\n"
            "（请确认 install.py 与 skills/ 在同一目录下，未被移动）"
        )
    skills = sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )
    if not skills:
        raise SystemExit(f"no SKILL.md found under {SKILLS_DIR}")
    return skills


def _is_managed(path: Path) -> bool:
    marker = path / MARKER_FILE
    if not marker.exists():
        return False
    try:
        data = _read_json(marker)
    except Exception:  # noqa: BLE001
        return False
    return data.get("package_id") == PACKAGE_ID


def _build_marker(
    skill_id: str,
    host_id: str,
    release: str,
    bundle_id: str,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "package_id": PACKAGE_ID,
        "host_id": host_id,
        "bundle_id": bundle_id,
        "skill_id": skill_id,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "release": release,
        "managed_by": f"install.py ({host_id} portable release)",
    }


def _detect_platform() -> str:
    """动态检测当前环境中安装了哪些智能体平台。

    通过探测平台安装目录来判断，而非查表。返回逗号分隔列表。
    """
    home = Path.home()
    found: list[str] = []

    if (home / ".claude").exists():
        found.append("myagents")
    if (home / ".codex").exists():
        found.append("codex")
    if (home / ".workbuddy").exists():
        found.append("workbuddy")
    if (home / ".kimi").exists():
        found.append("kimi-code")
    if (home / ".config" / "opencode").exists():
        found.append("opencode")
    if (home / ".openclaw").exists():
        found.append("openclaw")
    if (Path.cwd() / ".cursor").exists():
        found.append("cursor")

    return ",".join(found) if found else "unknown"


def _check_native_skill_support() -> bool:
    """动态检测是否有支持原生 Skill 发现的平台。"""
    return _detect_platform() != "unknown"


def _check_mcp_available() -> bool:
    """检测 MCP 客户端是否可用（Python 3.9+ 均可通过 stdio 对接 MCP server）。"""
    return sys.version_info >= (3, 9)


def _check_scheduler_available() -> bool:
    """动态检测当前环境是否有**平台级**定时调度能力。

    只探测 Unix crontab 与各平台的 tasks 配置目录。注意：不探测 Windows
    Task Scheduler——`schtasks /query` 在 Windows 上几乎总是成功（系统自带
    计划任务程序），它只能证明"系统存在调度器"，不能证明本 skillpack 的
    workflow 会被自动触发，探测它会把 Windows 用户全部误判为"已具备调度"。
    """
    home = Path.home()

    # Unix crontab
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, timeout=2
        )
        if result.returncode == 0:
            return True
    except Exception:  # noqa: BLE001
        pass

    # 各平台的 tasks/scheduled 目录
    task_dirs = [
        home / ".claude" / "tasks",
        home / ".codex" / "tasks",
        home / ".workbuddy" / "tasks",
        home / ".config" / "opencode" / "tasks",
        home / ".openclaw" / "tasks",
        home / ".kimi" / "tasks",
    ]
    return any(d.exists() for d in task_dirs)


def _has_workflows() -> bool:
    """本 plugin 是否包含 workflow 定义。"""
    return WORKFLOWS_DIR.exists() and any(WORKFLOWS_DIR.iterdir())


def _print_recommendation(
    platform: str,
    native: bool,
    scheduler: bool,
    has_wf: bool,
) -> None:
    """根据动态检测结果推荐最佳接入路径。"""
    print()
    print("=" * 60)
    print("推荐路径")
    print("=" * 60)

    if native:
        print(f"检测到平台: {platform}")
        print()
        print("路径 A: 原生 Skill 发现")
        print("  install.py 将 skills 安装到平台目录，平台自动识别 SKILL.md。")
        if has_wf:
            print()
            if scheduler:
                print("  检测到平台级调度能力；Workflow 是否能自动触发仍取决于平台。")
            else:
                print("  本 Plugin 包含定时 Workflow，但未检测到平台级调度能力。")
            print("  在 Legal Gateway 发布前，Workflow 需手动触发，或在平台自身的")
            print("  定时任务能力（如 MyAgents Task、cron）中配置。")
    else:
        print(f"检测到平台: {platform}")
        print()
        print("路径 B: MCP Gateway 统一接入")
        print("  当前平台不支持原生 Skill 发现。")
        print(f"  {GATEWAY_STATUS_NOTE}")
    print("=" * 60)


def _check_profile_home() -> None:
    """检查核心环境变量 LEGAL_AGENT_PROFILE_HOME 是否有落点。

    该变量是整套 skillpack 运行时中立设计的核心（profiles / 审计 / 产出的
    统一根目录），全库 500+ 处引用。脚本**不会**替用户设置环境变量，只在
    未设置时给出明确说明与建议默认值，避免路径以字面量形式悬空。
    """
    checks = [
        (PROFILE_HOME_VAR, str(Path.home() / ".legal-agent"),
         "全库 profiles/审计/产出的统一根目录"),
        ("LEGAL_AGENT_LOCAL_DATA_HOME", str(Path.home() / ".legal-agent" / "local-data"),
         "本地数据/工作成果落盘目录（检索与产出类 skill 使用）"),
    ]
    for var, default, desc in checks:
        if os.environ.get(var):
            print(f"{var} = {os.environ[var]}")
            continue
        suggested = os.path.expanduser(default)
        print(f"⚠ 环境变量 {var} 未设置（{desc}）。")
        print(f"  建议将其设为一个固定目录（推荐 {default}），例如：")
        print(f"    Windows PowerShell : setx {var} \"{suggested}\"")
        print(f"    Git Bash / Linux   : echo 'export {var}=\"{suggested}\"' >> ~/.bashrc")
    print("  未设置时，部分 skill 会把该路径当字面量字符串处理，产出可能落错位置。")


def cmd_check() -> int:
    """环境检测模式：动态探测 + 智能推荐。"""
    print("=" * 60)
    print("环境能力检测")
    print("=" * 60)

    platform = _detect_platform()
    native = _check_native_skill_support()
    scheduler = _check_scheduler_available()
    has_wf = _has_workflows()

    print(f"检测到平台:               {platform}")
    print(f"原生 Skill 发现:          {'是' if native else '否'}")
    print(f"定时调度器:               {'检测到' if scheduler else '未检测到'}")
    print(f"包含 Workflow:            {'是' if has_wf else '否'}")
    print()
    _check_profile_home()

    _print_recommendation(platform, native, scheduler, has_wf)
    return 0


def _copy_skill(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def _print_gateway_guide(reasons: list[str]) -> None:
    """如实告知 Gateway 状态与当前可行的替代方案。

    注意：Legal Gateway 尚未发布，**绝不**引导用户 pip install 不存在的包。
    """
    print()
    print("—" * 60)
    print("环境提示")
    for r in reasons:
        print(f"  - {r}")
    print()
    print(f"  {GATEWAY_STATUS_NOTE}")
    print("—" * 60)


def _backup_existing(dst: Path, dry_run: bool) -> Path | None:
    """覆盖前把已存在的目录改名为 .bak-<时间戳>，保留回滚能力。

    仅对非本包管理的目录调用（用户自建同名目录），给出可恢复路径；
    本包管理的目录直接覆盖即可（重装可再生成）。
    """
    if dry_run or not dst.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = dst.with_name(f"{dst.name}.bak-{stamp}")
    dst.rename(backup)
    return backup


def cmd_install(
    target_dir: Path,
    force: bool,
    dry_run: bool,
    host_id: str,
    release: str,
    bundle_id: str,
    host_override: str | None = None,
) -> int:
    bundled = _list_bundled_skills()
    summary = Summary()

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for source in bundled:
        skill_id = source.name
        dst = target_dir / skill_id

        if dst.exists() and not _is_managed(dst) and not force:
            summary.blocked += 1
            summary.details.append(
                f"BLOCK {skill_id}: 目标目录存在且不是本包管理；--force 才会覆盖"
                f"（覆盖前自动备份为 <name>.bak-<时间戳>）"
            )
            continue

        if dst.exists() and _is_managed(dst) and not force:
            summary.skipped += 1
            summary.details.append(
                f"SKIP  {skill_id}: 已是本包管理且未要求更新；--force 强制更新"
            )
            continue

        action = "UPDATE" if dst.exists() else "INSTALL"
        backup_note = ""
        if dst.exists() and not _is_managed(dst) and force:
            backup = _backup_existing(dst, dry_run)
            if backup is not None:
                backup_note = f"（原目录已备份: {backup.name}）"
                summary.details.append(f"BACKUP {skill_id}: 原非本包管理目录已备份")
        _copy_skill(source, dst, dry_run)
        if not dry_run:
            (dst / MARKER_FILE).write_text(
                json.dumps(
                    _build_marker(skill_id, host_id, release, bundle_id),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        if action == "INSTALL":
            summary.installed += 1
        else:
            summary.updated += 1
        prefix = "DRY-RUN " if dry_run else ""
        summary.details.append(f"{prefix}{action} {skill_id} -> {dst}{backup_note}")

    for line in summary.details:
        print(line)
    print()
    print(
        f"Summary: installed={summary.installed} updated={summary.updated} "
        f"skipped={summary.skipped} blocked={summary.blocked}"
    )

    # 安装位置 ⇄ 运行时读取目录核对（防止"安装成功但平台读不到 skill"）
    if not dry_run and summary.installed + summary.updated > 0:
        runtime_dir = _runtime_read_dir(host_id, host_override)
        print()
        print(f"✅ skill 已安装到：{target_dir}")
        if runtime_dir is not None:
            print(f"   目标平台运行时从此目录读取 skill：{runtime_dir}")
            if runtime_dir != target_dir:
                print()
                print("⚠ 警告：安装目录与本平台运行时读取目录不一致！")
                print(f"   实际装到：{target_dir}")
                print(f"   平台读取：{runtime_dir}")
                print("   平台很可能看不到刚装的 skill。请改用：")
                print(f"     python3 install.py --target {runtime_dir}")
                print("   或重启后确认 slash 命令是否出现；必要时手动把上面 skill 复制到'平台读取'目录。")
        else:
            print("   ⚠ 无法确定该平台运行时读取 skill 的目录（未指定 --host 且 manifest")
            print("   未声明 host_id）。请自行确认你所用运行时的 skill 目录与本安装目录一致；")
            print("   如不一致，把上面各 skill 目录移动/复制到运行时目录，或用 --target 重装。")

    # 安装后环境提示（Gateway 状态如实告知，不引导安装不存在的包）
    if not dry_run and summary.installed + summary.updated > 0:
        reasons: list[str] = []
        if _has_workflows() and not _check_scheduler_available():
            reasons.append("本 Plugin 含定时 Workflow，但平台未检测到调度能力")
        if not _check_native_skill_support():
            reasons.append("未检测到原生 Skill 发现平台")
        if reasons:
            _print_gateway_guide(reasons)
        _check_profile_home()

    if summary.blocked:
        print(
            "\n至少一个目标目录已存在且非本包管理；如果确定要覆盖，重试时加 --force。"
        )
        return 1
    return 0


def cmd_uninstall(target_dir: Path, dry_run: bool) -> int:
    if not target_dir.exists():
        print(f"target dir not present: {target_dir}（无可卸载内容）")
        return 0
    bundled = {p.name for p in _list_bundled_skills()}
    summary = Summary()

    for child in sorted(target_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name not in bundled:
            continue
        if not _is_managed(child):
            summary.blocked += 1
            summary.details.append(
                f"BLOCK {child.name}: 非本包安装的同名目录，跳过"
            )
            continue
        prefix = "DRY-RUN " if dry_run else ""
        summary.details.append(f"{prefix}REMOVE {child}")
        if not dry_run:
            shutil.rmtree(child)
        summary.removed += 1

    for line in summary.details:
        print(line)
    print()
    print(f"Summary: removed={summary.removed} blocked={summary.blocked}")
    if summary.blocked:
        print(
            "\n至少一个同名目录非本包管理，未删除。请检查后人工处理。"
        )
        return 1
    return 0


def cmd_list(target_dir: Path) -> int:
    bundled = sorted(p.name for p in _list_bundled_skills())
    print(f"Bundled skills: {len(bundled)} 个")
    print(f"Target dir:     {target_dir}")
    if not target_dir.exists():
        print("（目标目录不存在；下面所有项都显示 not-installed）\n")

    width = max((len(name) for name in bundled), default=20)
    header = f"{'skill_id':<{width}}  {'status':<15}  installed_at"
    print(header)
    print("-" * len(header))

    for skill_id in bundled:
        dst = target_dir / skill_id
        status = "not-installed"
        installed_at = ""
        if dst.exists():
            if _is_managed(dst):
                status = "managed"
                try:
                    marker = _read_json(dst / MARKER_FILE)
                    installed_at = marker.get("installed_at", "")
                except Exception:  # noqa: BLE001
                    status = "bad-marker"
            else:
                status = "unmanaged"
        print(f"{skill_id:<{width}}  {status:<15}  {installed_at}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="安装 / 卸载 / 查看 Legal Agent Skillpack 内的中国法 skill。",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="目标 skill 目录（支持 Git Bash 的 /d/foo 风格路径）；省略时按 host 选择。",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="显式指定目标平台（codex/workbuddy/myagents/kimi-code/opencode/openclaw/agents/cursor）；"
        "多平台并存时避免静默猜测的首选方式",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖目标目录中的同名 skill 目录——包括非本包管理的目录"
        "（非管理目录覆盖前自动备份为 <name>.bak-<时间戳>）",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="卸载所有本包管理的 skill（按 .legal-agent-skillpack-install.json 标记筛选）",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出 bundle 内每个 skill 在目标目录中的安装状态",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要执行的动作，不真的写入或删除",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="只检测环境能力，输出 Gateway 建议，不安装",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = _load_manifest()
    host_id = _resolve_host(manifest)
    release = manifest.get("source_commit") or manifest.get("generated_at") or "unknown"
    bundle_id = manifest.get("bundle_id") or "all"

    if args.check_only:
        return cmd_check()

    if args.target is not None:
        target_dir = _normalize_target_path(args.target)
    else:
        target_dir = _resolve_target_for_install(host_id, args.host)

    print(f"host_id:    {host_id}")
    print(f"bundle_id:  {bundle_id}")
    print(f"release:    {release}")
    print(f"target_dir: {target_dir}")
    print()
    if args.list:
        return cmd_list(target_dir)
    if args.uninstall:
        return cmd_uninstall(target_dir, args.dry_run)
    return cmd_install(target_dir, args.force, args.dry_run, host_id, release, bundle_id, args.host)


if __name__ == "__main__":
    raise SystemExit(main())
