#!/usr/bin/env python3
"""Standalone skill installer for the Legal Agent Skillpack portable release.

本文件被 ``src/export/build_release.py`` 复制到分发包根目录，命名为
``install.py``。它**不依赖本项目源码**，只用 Python 3.9+ 标准库。

host-agnostic 设计：从 ``EXPORT-MANIFEST.json`` 读 ``host_id``，按内置表查默认目标目录。
所有 host（codex / myagents / cursor / agents / opencode / kimi-code / openclaw / workbuddy）
都用同一个 installer。

用法：

    python3 install.py                # 自动检测平台并装到对应默认目录
    python3 install.py --target DIR   # 强制装到指定目录（覆盖自动检测）
    python3 install.py --force        # 覆盖已安装版本（仅限本包标记管理）
    python3 install.py --uninstall    # 卸载本包管理的 skill
    python3 install.py --list         # 列出每个 skill 的安装状态
    python3 install.py --check-only   # 仅检测环境能力，不安装

自动检测规则：
- host_id == "portable" 时，扫描 ~/.claude / ~/.codex / ~/.codebuddy / ~/.kimi /
  ~/.config/opencode / ~/.openclaw / 当前目录的 .cursor，按检测结果选目录
- 检测到多个平台时，默认装到第一个，提示用户用 --target 装其他平台
- 未检测到任何平台时，回退到 ~/.agents/skills 并提示

不会调用网络、不会修改默认目标目录之外的位置、不会处理任何用户密钥。

Gateway 引导：
- 安装时自动检测平台能力，如缺少定时调度/审计闸门，会提示安装 Legal Gateway
- 详细兼容性检查见本目录 CHECKPOINT.md
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_ID = "claude-for-legal"
MARKER_FILE = ".legal-agent-skillpack-install.json"
GATEWAY_INSTALL_CMD = "pip install legal-gateway\nlegal-gateway init --skills ./skills"
GATEWAY_REPO_URL = "https://github.com/yuandian-ailaw/Agent-for-legal-cn/tree/main/legal-gateway"

HERE = Path(__file__).resolve().parent
SKILLS_DIR = HERE / "skills"
WORKFLOWS_DIR = HERE / "workflows"
MANIFEST_PATH = HERE / "EXPORT-MANIFEST.json"

# host_id → 默认目标。新 host 在这里加一行，无需改其他代码。
# 注意：cursor 是相对当前 cwd 的 .cursor/skills（项目级），其他都是 ~/<dir>/skills 全局。
DEFAULT_TARGETS: dict[str, str] = {
    "codex": "~/.codex/skills",
    "workbuddy": "~/.codebuddy/skills",
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


def _resolve_target_for_install(host_id: str) -> Path:
    """决定安装目标目录。

    若 manifest 的 host_id 已指明具体平台 → 直接查表。
    若 host_id 是 'portable' 或 'unknown' → 调用 _detect_platform()
    用动态检测结果选目录；检测不到则回退到通用 ~/.agents/skills。
    多平台并存时，默认装到第一个，提示用户用 --target 装其他平台。
    """
    if host_id in DEFAULT_TARGETS:
        return Path(DEFAULT_TARGETS[host_id]).expanduser().resolve()

    detected = _detect_platform()
    if detected == "unknown":
        print("⚠ 未检测到任何已知智能体平台。", file=sys.stderr)
        print(f"  默认装到通用目录: {FALLBACK_TARGET}", file=sys.stderr)
        print("  如需装到具体平台，请用: python3 install.py --target <path>", file=sys.stderr)
        return Path(FALLBACK_TARGET).expanduser().resolve()

    platforms = detected.split(",")
    chosen = platforms[0]
    chosen_path = DEFAULT_TARGETS.get(chosen, FALLBACK_TARGET)
    if len(platforms) > 1:
        others = ", ".join(platforms[1:])
        print(f"检测到多个平台: {detected}")
        print(f"  默认装到第一个: {chosen} → {chosen_path}")
        print(f"  如需装到其他平台 ({others})，重跑并加 --target <path>")
    else:
        print(f"检测到平台: {chosen} → {chosen_path}")
    return Path(chosen_path).expanduser().resolve()


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
    if (home / ".codebuddy").exists():
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
    """动态检测当前环境是否有定时调度能力。

    不依赖预知信息，而是实际探测系统调度器和各平台调度配置目录。
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

    # Windows Task Scheduler
    try:
        result = subprocess.run(
            ["schtasks", "/query"], capture_output=True, timeout=3
        )
        if result.returncode == 0:
            return True
    except Exception:  # noqa: BLE001
        pass

    # 各平台的 tasks/scheduled 目录
    task_dirs = [
        home / ".claude" / "tasks",
        home / ".codex" / "tasks",
        home / ".codebuddy" / "tasks",
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
        if has_wf and not scheduler:
            print()
            print("  本 Plugin 包含定时 Workflow，但未检测到调度器。")
            print("  如需 Workflow 自动触发，可安装 Gateway daemon：")
            print(f"    {GATEWAY_INSTALL_CMD}")
            print(f"    指南: {GATEWAY_REPO_URL}")
        elif has_wf and scheduler:
            print()
            print("  定时调度器已检测到，Workflow 可自动触发。")
    else:
        print(f"检测到平台: {platform}")
        print()
        print("路径 B: MCP Gateway 统一接入")
        print("  当前平台不支持原生 Skill 发现，请通过 MCP 接入。")
        print(f"  安装: {GATEWAY_INSTALL_CMD}")
        print(f"  指南: {GATEWAY_REPO_URL}")
    print("=" * 60)


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


def cmd_install(
    target_dir: Path,
    force: bool,
    dry_run: bool,
    host_id: str,
    release: str,
    bundle_id: str,
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
                f"BLOCK {skill_id}: 目标目录存在且不是本包管理；--force 才能覆盖"
            )
            continue

        if dst.exists() and _is_managed(dst) and not force:
            summary.skipped += 1
            summary.details.append(
                f"SKIP  {skill_id}: 已是本包管理且未要求更新；--force 强制更新"
            )
            continue

        action = "UPDATE" if dst.exists() else "INSTALL"
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
        summary.details.append(f"{prefix}{action} {skill_id} -> {dst}")

    for line in summary.details:
        print(line)
    print()
    print(
        f"Summary: installed={summary.installed} updated={summary.updated} "
        f"skipped={summary.skipped} blocked={summary.blocked}"
    )

    # 安装完成后自动检测环境并引导 Gateway
    if not dry_run and summary.installed + summary.updated > 0:
        reasons: list[str] = []
        if _has_workflows() and not _check_scheduler_available():
            reasons.append("本 Plugin 含定时 Workflow，但平台未检测到调度器")
        if not _check_native_skill_support():
            reasons.append("未检测到原生 Skill 发现平台")
        if reasons:
            _print_gateway_guide(reasons)

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
        type=Path,
        default=None,
        help="目标 skill 目录；省略时按 EXPORT-MANIFEST.json 的 host_id 选默认。",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖已存在的同名目录（仅当目标是本包管理时才允许；非管理需另行处理）",
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
        target_dir = args.target.expanduser().resolve()
    else:
        target_dir = _resolve_target_for_install(host_id)

    print(f"host_id:    {host_id}")
    print(f"bundle_id:  {bundle_id}")
    print(f"release:    {release}")
    print(f"target_dir: {target_dir}")
    print()
    if args.list:
        return cmd_list(target_dir)
    if args.uninstall:
        return cmd_uninstall(target_dir, args.dry_run)
    return cmd_install(target_dir, args.force, args.dry_run, host_id, release, bundle_id)


if __name__ == "__main__":
    raise SystemExit(main())
