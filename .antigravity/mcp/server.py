#!/usr/bin/env python3
"""Small, dependency-free MCP stdio server for Antigravity Squad artifacts."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "2024-11-05"
AGENTS = {
    "pm": "produto/pesquisa-de-campo.md",
    "coord": "coordenacao/coord.md",
    "designer": "design/direcao-visual-e-marca.md",
    "design_system": "design/DESIGN.md",
    "dba": "dados/dba.md",
    "backend": "backend/backend.md",
    "frontend": "frontend/frontend.md",
    "frontend_reviewer": "frontend/revisao-visual.md",
    "appsec": "seguranca/appsec.md",
    "qa": "qualidade/qa.md",
    "devops": "operacao/devops.md",
}
SECTIONS = "## Contexto e evidências\n\n[Fatos, fontes e hipóteses.]\n\n## Decisões e recomendações\n\n[Pontos relevantes.]\n\n## O que precisa ser feito\n\n[Tarefas e critérios.]\n\n## Plano e dependências\n\n[Plano e dependências.]\n\n## O que foi feito\n\nNenhuma implementação de produto nesta fase.\n\n## Validação e evidências\n\nNão executado.\n\n## Pendências e riscos\n\n[Pendências.]\n\n## Fontes\n\n[URLs diretas e data de acesso, se houver.]\n"


class SquadError(Exception):
    pass


def project_root(value: str) -> Path:
    if not value or "\x00" in value:
        raise SquadError("project_root é obrigatório")
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise SquadError("project_root precisa ser uma pasta existente")
    return root


def safe_path(root: Path, relative: str, *, allow_missing: bool = True) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or not relative or "\x00" in relative:
        raise SquadError("Use um caminho relativo dentro do projeto-alvo")
    # Resolve existing parents too, preventing symlink escapes.
    resolved = (root / candidate).resolve(strict=not allow_missing)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SquadError("Caminho fora da pasta do projeto-alvo") from exc
    return resolved


def inspect_project(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    ignored = {".git", ".agents", "node_modules", ".venv", "bin", "obj"}
    files: list[str] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(names):
            path = Path(current, name)
            rel = path.relative_to(root).as_posix()
            files.append(rel)
            if len(files) >= 5000:
                break
        if len(files) >= 5000:
            break
    markers = {
        ".NET": ["*.sln", "*.slnx", "*.csproj"], "Node": ["package.json"],
        "Python": ["pyproject.toml", "requirements.txt", "setup.py"],
        "Rust": ["Cargo.toml"], "Go": ["go.mod"],
    }
    stacks = [label for label, patterns in markers.items()
              if any(Path(p).match(pattern) for p in files for pattern in patterns)]
    return {"project_root": str(root), "file_count_listed": len(files), "truncated": len(files) >= 5000,
            "stack_markers": stacks, "files": files}


def initialize_docs(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    docs = safe_path(root, ".agentes")
    docs.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    index = "# Documentação do Antigravity Squad\n\nDemanda: [preencher]\n\n## Relatórios\n\n" + "".join(
        f"- [{name}](./{path})\n" for name, path in AGENTS.items()) + "\n## Roadmap\n\n- [Roadmap](./coordenacao/roadmap.md)\n"
    for relative in ["README.md", *AGENTS.values(), "coordenacao/roadmap.md", "PROJECT_MAP.md"]:
        target = safe_path(root, f".agentes/{relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        if relative == "README.md":
            content = index
        elif relative == "coordenacao/roadmap.md":
            content = "# Roadmap\n\n## Contexto e decisões\n\n[Contexto, stack observada e decisões.]\n\n## Itens\n\n[IDs, prioridade, status, escopo, dependências, critérios de aceite, validação e evidências.]\n"
        elif relative == "PROJECT_MAP.md":
            content = "# PROJECT_MAP — Índice confirmado do projeto\n\nConfirme caminhos e contratos antes de depender deste mapa.\n\n## Telas e componentes\n\n| Área | Caminho | Estados | Verificado em |\n|---|---|---|---|\n\n## Rotas e APIs\n\n| Fluxo | Método/rota | Contrato | Autorização | Evidência |\n|---|---|---|---|---|\n\n## Dados e integrações\n\n| Recurso | Fonte | Consumidores | Observações |\n|---|---|---|---|\n\n## Testes e operação\n\n| Escopo | Comando/documento | Resultado |\n|---|---|---|\n"
        else:
            agent = next(k for k, v in AGENTS.items() if v == relative)
            content = f"# {agent.replace('_', ' ').title()} — Relatório\n\n- **Status:** PLANEJADO\n- **Atualizado em:** {date.today().isoformat()}\n- **Demanda/roadmap:** [preencher]\n- **Responsabilidade:** {agent}\n\n" + SECTIONS
        target.write_text(content, encoding="utf-8", newline="\n")
        created.append(f".agentes/{relative}")
    return {"project_root": str(root), "created": created, "preserved_existing": True}


def update_report(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    agent, content = args.get("agent"), args.get("content")
    if agent not in AGENTS:
        raise SquadError(f"agent deve ser um de: {', '.join(AGENTS)}")
    if not isinstance(content, str) or not content.strip():
        raise SquadError("content precisa conter o relatório completo")
    rel = f".agentes/{AGENTS[agent]}"
    target = safe_path(root, rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return {"updated": rel}


def update_roadmap(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    content = args.get("content")
    if not isinstance(content, str) or not content.strip():
        raise SquadError("content precisa conter o roadmap completo")
    target = safe_path(root, ".agentes/coordenacao/roadmap.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return {"updated": ".agentes/coordenacao/roadmap.md"}


def validate_artifacts(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    required = [".agentes/README.md", ".agentes/coordenacao/roadmap.md",
                *[f".agentes/{p}" for p in AGENTS.values()]]
    results = []
    required_sections = ["Contexto e evidências", "O que precisa ser feito", "Plano", "O que foi feito", "Validação", "Pendências"]
    evidence_links = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    issues: list[str] = []
    for rel in required:
        path = safe_path(root, rel)
        exists = path.is_file()
        content = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        sections_missing = [heading for heading in required_sections if f"## {heading}" not in content] if rel in [f".agentes/{p}" for p in AGENTS.values()] else []
        broken_links = []
        for target in evidence_links.findall(content):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            try:
                linked = safe_path(root, (path.parent / target).relative_to(root).as_posix())
                if not linked.exists():
                    broken_links.append(target)
            except (ValueError, SquadError):
                broken_links.append(target)
        result = {"path": rel, "exists": exists, "non_empty": bool(content.strip()),
                  "missing_sections": sections_missing, "broken_local_links": broken_links,
                  "has_validation_evidence_section": "Validação" in content or "ValidaÃ§Ã£o" in content}
        results.append(result)
        if not exists or not content.strip():
            issues.append(f"Ausente ou vazio: {rel}")
        if sections_missing:
            issues.append(f"Seções ausentes em {rel}: {', '.join(sections_missing)}")
        if broken_links:
            issues.append(f"Links locais sem evidência em {rel}: {', '.join(broken_links)}")
    return {"valid": not issues, "issues": issues, "artifacts": results}


TOOLS = [
    {"name": "inspect_project", "description": "Lista arquivos do projeto-alvo e detecta marcadores de stack sem alterar arquivos.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "initialize_squad_docs", "description": "Cria .agentes com índice, relatórios, roadmap e mapa; preserva arquivos existentes.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "update_agent_report", "description": "Cria ou substitui o relatório completo de um agente em .agentes/.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "agent": {"type": "string", "enum": list(AGENTS)}, "content": {"type": "string"}}, "required": ["project_root", "agent", "content"]}},
    {"name": "update_roadmap", "description": "Cria ou substitui .agentes/coordenacao/roadmap.md.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "content": {"type": "string"}}, "required": ["project_root", "content"]}},
    {"name": "validate_squad_artifacts", "description": "Verifica existência, seções mínimas dos relatórios e destinos de links locais usados como evidência.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
]
HANDLERS = {"inspect_project": inspect_project, "initialize_squad_docs": initialize_docs,
            "update_agent_report": update_report, "update_roadmap": update_roadmap,
            "validate_squad_artifacts": validate_artifacts}


def respond(message: dict[str, Any]) -> dict[str, Any] | None:
    method, ident, params = message.get("method"), message.get("id"), message.get("params", {})
    if method == "notifications/initialized" or method == "notifications/cancelled":
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": ident, "result": {"protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "antigravity-squad", "version": "1.0.0"}}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": ident, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": ident, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        try:
            if name not in HANDLERS:
                raise SquadError(f"Ferramenta desconhecida: {name}")
            result = HANDLERS[name](params.get("arguments", {}))
            content = json.dumps(result, ensure_ascii=False, indent=2)
            return {"jsonrpc": "2.0", "id": ident, "result": {"content": [{"type": "text", "text": content}], "structuredContent": result}}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": ident, "result": {"isError": True, "content": [{"type": "text", "text": str(exc)}]}}
    if ident is not None:
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": f"Método desconhecido: {method}"}}
    return None


def main() -> None:
    for line in sys.stdin:
        try:
            result = respond(json.loads(line))
            if result is not None:
                sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
