#!/usr/bin/env python3
"""法条引用时效门禁 — agent-for-legal-cn

为什么需要它：法条是"有有效期的数据"。2026-09 第三方审计发现《律师法》第38条
失效 4 天全库无人知晓（18 处引用未迁移）、已废止的《合同法》仍在被引用、
《商标法》引用未锁版本（2026 修订版 2027-01-01 施行且条号重排）。
本脚本把这些检查固化为发布门禁。

用法：
    python3 tools/verify_citations.py                    # 离线审计（CI 默认）
    python3 tools/verify_citations.py --json-out todo.json
    python3 tools/verify_citations.py --pack legal-skillpack-ip-legal
    python3 tools/verify_citations.py --verbose

离线判定（exit 0 通过 / 1 发现问题）：
  FAIL  引用了 banned 表中已废止法规（无有效历史语境标注）
  FAIL  引用了存在"已公布未施行"新修订版且未锁版本的法规（裸《商标法》第X条）
  FAIL  出现域外法引用（DSA/U.S.C./英文条款引用）但未标注"外国法对照"
  WARN  引用了登记表中不存在的法规名（需人工登记或纠正别名）
  INFO  全部引用清单（--verbose 显示）

在线活库核验不在本脚本内：运行 --json-out 生成待核验清单后，用元典 MCP
（yuandian_rh_ft_detail，逐条查 sxx 字段）批量核验，结果回写
docs/legal-citations/registry.yaml 的 last_verified。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要 PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "legal-citations" / "registry.yaml"

# 《X法》第Y条：X 最多 40 字；Y 支持阿拉伯与中文数字
CITE_PAT = re.compile(r"《([^》\n]{2,40})》(?:（([^（）]{1,20})）)?第\s*([0-9]+|[一二三四五六七八九十百零]+)\s*条")
# 域外法特征。注意：§ 符号是中国法规与合同通用的条款编号，不作为域外法特征。
FOREIGN_PAT = re.compile(
    r"数字服务法|Digital Services Act|\bDSA\b|U\.S\.C\.|《统一商法典》|UCC\b|"
    r"美国《?(?:专利法|版权法|商标法)|Del\.?\s(?:Code|Ct)|Cal\.?\s(?:Civ|Pen|Bus)"
)
FOREIGN_MARK = re.compile(r"外国法对照|非中国法依据|域外对照")
# 历史语境豁免：描述"已废止/已迁移"的句子不是失效引用
HISTORY_MARK = re.compile(r"已废止|已失效|已随|整体废止|已由《|废止|原《|已由.{0,20}取代|迁至|条号迁移")

CN_NUM = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9}
CN_UNIT = {"十": 10, "百": 100}


def cn2int(s: str) -> int:
    if s.isdigit():
        return int(s)
    total, num = 0, 0
    for ch in s:
        if ch in CN_NUM:
            num = CN_NUM[ch]
        elif ch in CN_UNIT:
            u = CN_UNIT[ch]
            total += (num or 1) * u
            num = 0
    return total + num


class Registry:
    def __init__(self, path: Path):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.migrated: dict[str, dict[str, str]] = {}   # 标准法规名 -> {旧条号: 新条号}
        self.short_aliases: dict[str, str] = {}          # 短别名 -> 标准名（用于无书名号宽松抽取）
        self.by_alias: dict[str, dict] = {}
        for reg in data.get("regulations", []):
            entry = {"standard": reg["name"], "reg": reg}
            self.by_alias[reg["name"]] = entry
            for a in reg.get("aliases", []):
                self.by_alias[a] = entry
                self.short_aliases[a] = reg["name"]
            if reg.get("migrated_articles"):
                self.migrated[reg["name"]] = {str(k): v for k, v in reg["migrated_articles"].items()}
        self.banned: dict[str, dict] = {}
        for b in data.get("banned", []):
            entry = {"standard": b["name"], "banned": b}
            self.banned[b["name"]] = entry
            for a in b.get("aliases", []):
                self.banned[a] = entry

    def lookup(self, name: str):
        """返回 ('ok', entry) / ('banned', entry) / ('unknown', None)"""
        if name in self.banned:
            return "banned", self.banned[name]
        if name in self.by_alias:
            return "ok", self.by_alias[name]
        return "unknown", None


LOOSE_CITE_PAT = re.compile(r"(律师法)第\s*([0-9]+|[一二三四五六七八九十百零]+)\s*条")
# "尚未施行"标注过期：施行日已过 7 天以上仍标"尚未施行"
STALE_EFFECTIVE_PAT = re.compile(r"[（(](\d{4}-\d{2}-\d{2})[^）\n]{0,30}尚未施行")
STALE_GRACE_DAYS = 7


def check_stale_effective(pack: str | None) -> list[str]:
    """施行状态过期检查：正文标注"（日期，尚未施行）"而施行日已过 -> FAIL。"""
    import datetime as _dt
    today = _dt.date.today()
    fails = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if pack and not rel.startswith(pack):
            continue
        if any(rel.startswith(x) or rel == x for x in GOVERNANCE_EXEMPT):
            continue
        try:
            for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                for m in STALE_EFFECTIVE_PAT.finditer(line):
                    eff = _dt.date.fromisoformat(m.group(1))
                    if (today - eff).days > STALE_GRACE_DAYS:
                        fails.append(
                            f"FAIL 施行状态过期: {rel}:{lineno}  （标注施行日 {m.group(1)} 已过 "
                            f"{(today - eff).days} 天仍写'尚未施行'——须更新为现行有效）"
                        )
        except Exception:
            continue
    return fails


def strip_version(name: str) -> tuple[str, bool]:
    """《商标法》（2019修正）→ ('商标法', True)。识别全角/半角括号内版本注记。"""
    m = re.match(r"^(.*?)[\(（]([^\)）]{2,20})[\)）]\s*$", name.strip())
    if m:
        return m.group(1).strip(), True
    return name.strip(), False


# 治理文件豁免：其正文合法记载历史条号/废止事实（问题清单、示例、迁移记录），不参与门禁
GOVERNANCE_EXEMPT = (
    "docs/legal-references.md",
    "docs/legal-citations/",
    "tools/",
)


def load_citations(pack: str | None) -> list[dict]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if pack and not rel.startswith(pack):
            continue
        if "/myagents_files/" in rel or any(rel.startswith(x) or rel == x for x in GOVERNANCE_EXEMPT):
            continue
        if "docs/schemas/" in rel or rel.endswith(".schema.yaml"):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in CITE_PAT.finditer(line):
                raw_name, ver_note, art = m.group(1), m.group(2), m.group(3)
                name, version_locked = strip_version(raw_name)
                version_locked = version_locked or bool(ver_note)
                out.append({
                    "file": rel,
                    "line": lineno,
                    "regulation_raw": raw_name,
                    "regulation": name,
                    "version_locked": version_locked,
                    "article": cn2int(art),
                    "article_display": f"第{art}条",
                    "context": line.strip()[:160],
                })
    return out


def load_loose_variants(pack: str | None) -> list[dict]:
    """抽取无书名号变体（如"律师法第38条"）：短别名 + 第N条。仅用于迁移黑名单检查。"""
    import re as _re
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if pack and not rel.startswith(pack):
            continue
        if any(rel.startswith(x) or rel == x for x in GOVERNANCE_EXEMPT):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in LOOSE_CITE_PAT.finditer(line):
                out.append({"file": rel, "line": lineno,
                            "regulation_raw": m.group(1), "article": cn2int(m.group(2)),
                            "article_display": f"第{m.group(2)}条", "context": line.strip()[:160],
                            "version_locked": False, "regulation": m.group(1)})
    return out


def check(cites: list[dict], reg: Registry, verbose: bool,
          pack: str | None = None) -> tuple[list[str], list[dict]]:
    fails: list[str] = []
    unknown_regs: set[str] = set()
    for c in cites:
        where = f'{c["file"]}:{c["line"]}  《{c["regulation_raw"]}》{c["article_display"]}'
        kind, entry = reg.lookup(c["regulation"])

        if kind == "banned":
            # 历史语境豁免：说明"已废止/迁移"的句子不算失效引用
            if HISTORY_MARK.search(c["context"]):
                continue
            # 外国法已标注豁免
            if FOREIGN_MARK.search(c["context"]):
                continue
            fails.append(f"FAIL banned-法规被引用: {where}")
            continue

        if kind == "unknown":
            unknown_regs.add(c["regulation"])
            continue

        # 已迁移条号判定（版本敏感）：旧条号+未锁版本 -> FAIL；锁旧版(<since) -> 合法历史引用；
        # 锁新版(>=since)却用旧条号 -> FAIL（版本与条号不匹配）；新条号 -> PASS
        std = entry["standard"]
        mig = reg.migrated.get(std, {}).get(str(c["article"]))
        if mig:
            since_year = int(str(mig["since"])[:4])
            m = re.search(r"[（(](\d{4})", c.get("regulation_raw") or "")
            locked_year = int(m.group(1)) if m else None
            if not c["version_locked"]:
                fails.append(
                    f"FAIL 已迁移条号(未锁版本): {where}  （{std} 第{c['article']}条自 {mig['since']} 起重排为第{mig['to']}条；"
                    f"现行条号见 docs/legal-citations/registry.yaml 的 migrated_articles）"
                )
                continue
            if locked_year is not None and locked_year >= since_year:
                fails.append(
                    f"FAIL 版本条号不匹配: {where}  （锁了 {locked_year} 年版本却用旧条号第{c['article']}条；该版次应为第{mig['to']}条）"
                )
                continue

        reginfo = entry["reg"]
        pending = reginfo.get("pending_effective_date")
        if pending and not c["version_locked"]:
            fails.append(
                f"FAIL 未锁版本: {where}  （{reginfo.get('pending_version','')} 将于 {pending} 施行，"
                f"施行前引用必须写明现行版本，如《{reginfo['name']}》（{reginfo.get('current_version','')}）{c['article_display']}）"
            )

    # 域外法标注检查（按行扫描，独立于《》条号模式）
    foreign_fails = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if pack and not rel.startswith(pack):
            continue
        if any(rel.startswith(x) or rel == x for x in GOVERNANCE_EXEMPT):
            continue
        try:
            for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if FOREIGN_PAT.search(line) and not FOREIGN_MARK.search(line):
                    # 同文件其他行有全局说明也可豁免：查全文
                    full = p.read_text(encoding="utf-8")
                    if FOREIGN_MARK.search(full):
                        continue
                    foreign_fails.append(
                        f"FAIL 域外法未标注: {rel}:{lineno}  （须注明'外国法对照，非中国法依据'）"
                    )
        except Exception:
            continue
    # 去重（同一文件多行命中只报前 5 行）
    seen_files: dict[str, int] = {}
    for f in foreign_fails:
        key = f.split(":")[0]
        seen_files[key] = seen_files.get(key, 0) + 1
        if seen_files[key] <= 5:
            fails.append(f)

    warns = [f"WARN 未登记法规(请补 registry.yaml): 《{r}》" for r in sorted(unknown_regs)]
    if verbose:
        for c in cites:
            print(f'INFO {c["file"]}:{c["line"]} 《{c["regulation"]}》{c["article_display"]}')
    return fails + warns, cites


def main() -> int:
    ap = argparse.ArgumentParser(description="法条引用时效门禁（离线审计）")
    ap.add_argument("--pack", default=None, help="只审计指定前缀的 pack，如 legal-skillpack-ip-legal")
    ap.add_argument("--json-out", default=None, help="输出待核验清单 JSON 路径")
    ap.add_argument("--check-baseline", action="store_true",
                    help="额外校验各 profile 目录下的 legal-baseline.yaml（可解析+必填字段+锚点带 validity_window）")
    ap.add_argument("--verbose", action="store_true", help="打印全部引用清单")
    args = ap.parse_args()

    reg = Registry(REGISTRY)
    cites = load_citations(args.pack) + load_loose_variants(args.pack)
    problems, _ = check(cites, reg, args.verbose, args.pack)

    problems += check_stale_effective(args.pack)

    if getattr(args, "check_baseline", False):
        base_dir = os.environ.get("LEGAL_AGENT_PROFILE_HOME")
        candidates = []
        if base_dir and Path(base_dir).exists():
            candidates += list(Path(base_dir).glob("*/legal-baseline.yaml"))
            candidates += list(Path(base_dir).glob("legal-baseline.yaml"))
        for bp in candidates:
            try:
                data = yaml.safe_load(bp.read_text(encoding="utf-8"))
            except Exception as e:
                problems.append(f"FAIL baseline 不可解析: {bp}（{str(e)[:80]}）——损坏的 baseline 等同无基准")
                continue
            for field in ("schema_version", "confirmed_at", "confirmed_by", "freshness_window", "source"):
                if not isinstance(data, dict) or field not in data:
                    problems.append(f"FAIL baseline 缺字段 {field}: {bp}")
            for a in (data.get("anchors") or []) if isinstance(data, dict) else []:
                if not a.get("validity_window"):
                    problems.append(f"FAIL baseline 锚点缺 validity_window: {bp} :: {a.get('id')}")
        print(f"baseline 校验：检查 {len(candidates)} 个文件")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps({"generated_by": "verify_citations.py",
                        "total_citations": len(cites),
                        "citations": cites}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"待核验清单已写入: {args.json_out}（共 {len(cites)} 处引用）")

    print()
    print(f"引用总数: {len(cites)}   问题: {len(problems)}")
    for p in problems:
        print(f"  {p}")
    if problems:
        print()
        print("❌ 门禁未通过——发布前请处理上述问题（历史语境豁免规则见脚本头部说明）")
        return 1
    print("✅ 门禁通过：无废止法规引用、无未锁版本引用、域外法均已标注")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
