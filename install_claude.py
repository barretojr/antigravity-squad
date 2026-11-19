#!/usr/bin/env python3
"""Instala o Squad para o Claude Code (skills, agentes e servidor MCP opcional).

Uso:
  python install_claude.py --project C:/Projetos/MinhaApp   # .claude/ dentro do projeto
  python install_claude.py --global                         # ~/.claude/
Opções:
  --with-heavy-skills   inclui taste-skill, design-taste-frontend e playwright-cli (~100 MB)
  --register-mcp        executa `claude mcp add` (escopo local ao projeto; só vale com --project)
Sem dependências externas. Os agentes são convertidos para o formato do Claude Code e só são
acionados quando a skill squad os chama (a descrição de cada um diz isso).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "squad-kit"
LIGHT_SKILLS = ["squad", "product-research", "product-brand-design", "quality-validation",
                "security-validation", "frontend-integration", "design-reference", "spatial-design"]
HEAVY_SKILLS = ["design-taste-frontend", "taste-skill", "playwright-cli"]
DROP_KEYS = ("subagent:", "mainAgent:", "inheritCustomizations:", "commandExecutionPolicy:")
PREFIX = "[squad] Use SOMENTE quando a skill squad chamar este agente pelo nome. "


def convert_agent(text: str) -> str:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return text
    head, sep, body = text[3:].partition("\n---")
    out, skipping_list = [], False
    for line in head.splitlines():
        if skipping_list and (line.startswith(" ") or line.startswith("-")):
            continue
        skipping_list = False
        if line.startswith("skills:"):
            skipping_list = True
            continue
        if line.startswith(DROP_KEYS):
            continue
        if line.startswith("description:"):
            line = "description: " + _yaml_quote(PREFIX + line[len("description:"):].strip())
        out.append(line)
    return "---" + "\n".join(out) + "\n---" + body


def _yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    where = ap.add_mutually_exclusive_group(required=True)
    where.add_argument("--project", help="raiz do projeto-alvo")
    where.add_argument("--global", dest="is_global", action="store_true", help="instala em ~/.claude")
    ap.add_argument("--with-heavy-skills", action="store_true")
    ap.add_argument("--register-mcp", action="store_true")
    args = ap.parse_args()

    if not SRC.is_dir():
        print(f"Pasta fonte não encontrada: {SRC}", file=sys.stderr)
        return 1
    if args.is_global:
        base = Path.home() / ".claude"
    else:
        proj = Path(args.project).expanduser().resolve()
        if not proj.is_dir():
            print(f"Projeto não encontrado: {proj}", file=sys.stderr)
            return 1
        base = proj / ".claude"

    skills = LIGHT_SKILLS + (HEAVY_SKILLS if args.with_heavy_skills else [])
    for name in skills:
        if (SRC / "skills" / name).is_dir():
            copy_tree(SRC / "skills" / name, base / "skills" / name)
    rules = SRC / "rules" / "squad-context.md"
    if rules.is_file():
        shutil.copyfile(rules, base / "skills" / "squad" / "references" / "squad-rules.md")

    (base / "agents").mkdir(parents=True, exist_ok=True)
    for agent in sorted((SRC / "agents").glob("*.md")):
        (base / "agents" / agent.name).write_text(convert_agent(agent.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")

    (base / "mcp").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC / "mcp" / "server.py", base / "mcp" / "server.py")
    server = (base / "mcp" / "server.py").as_posix()

    if not args.is_global:
        gi = proj / ".gitignore"
        current = gi.read_text(encoding="utf-8", errors="ignore") if gi.is_file() else ""
        if ".squad/" not in current.splitlines():
            with open(gi, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(("\n" if current and not current.endswith("\n") else "") + "\n# Squad artifacts\n.squad/\n")

    print(f"Skills ({len(skills)}), agentes e servidor MCP instalados em {base}")
    cmd = ["claude", "mcp", "add", "squad", "--scope", "local", "--", sys.executable, server]
    if args.register_mcp and not args.is_global:
        if shutil.which("claude"):
            subprocess.run(cmd, cwd=str(proj), check=False)
        else:
            print("`claude` não está no PATH; rode manualmente o comando abaixo.")
    print("\nO MCP é opcional e NÃO foi registrado globalmente. Para ativá-lo só no projeto que precisar, rode dentro dele:")
    print("  " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    print("\nUse: /squad <seu pedido>  ou  \"use a skill squad e crie ...\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
