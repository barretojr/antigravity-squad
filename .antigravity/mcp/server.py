#!/usr/bin/env python3
"""Small, dependency-free MCP stdio server for Antigravity Squad artifacts and architecture auditing."""
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

BASE_SECTIONS = """## Contexto e evidências

[Fatos, fontes e hipóteses.]

## Decisões e recomendações

[Pontos relevantes.]

## O que precisa ser feito

[Tarefas e critérios.]

## Plano e dependências

[Plano e dependências.]

## O que foi feito

Nenhuma implementação de produto nesta fase.

## Validação e evidências

Não executado.

## Pendências e riscos

[Pendências.]

## Fontes

[URLs diretas e data de acesso, se houver.]
"""

ROLE_EXTRA_SECTIONS = {
    "pm": """## Pesquisa de APIs e Integrações

[Mapeamento das APIs oficiais de marketplaces (Mercado Livre, Shopee, Amazon, TikTok) e WhatsApp Business Cloud API oficial.]

## Gestão de Credenciais e Configurações

[Especificação da tela/fluxo onde o usuário configura chaves de API, webhooks e credenciais com segurança.]
""",
    "dba": """## Mecanismo de Persistência Físico

[Onde e como os dados residem fisicamente (PostgreSQL 17, SQLite, etc.). Não aprovar persistência puramente em memória List<T> como concluída.]
""",
    "appsec": """## Autenticação e Criptografia

[Fluxo de login/sessão, hashing seguro de senhas (BCrypt, Argon2, PBKDF2), proteção de tokens e criptografia de credenciais de terceiros.]
""",
    "frontend": """## Linguagem do Usuário e Anti-Jargão

[Garantia de que a interface não exibe termos técnicos, badges de framework (.NET, React, etc.) ou jargões de backend.]
""",
    "designer": """## Linguagem do Usuário e Anti-Jargão

[Vocabulário estritamente voltado ao domínio de negócio e à jornada do usuário, eliminando tech-jargon.]
""",
}

ROLE_REQUIRED_HEADINGS = {
    "pm": ["Pesquisa de APIs e Integrações", "Gestão de Credenciais e Configurações"],
    "dba": ["Mecanismo de Persistência Físico"],
    "appsec": ["Autenticação e Criptografia"],
    "frontend": ["Linguagem do Usuário e Anti-Jargão"],
    "designer": ["Linguagem do Usuário e Anti-Jargão"],
}

JARGON_PATTERN = re.compile(
    r'(\.NET\s*10|React\s*19|no\s+Backend|API\s+Conectada|Backend\s+Conectado|Vue\s*3|Angular\s*1)',
    re.IGNORECASE
)


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
    resolved = (root / candidate).resolve(strict=not allow_missing)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SquadError("Caminho fora da pasta do projeto-alvo") from exc
    return resolved


def find_ui_jargon_leaks(root: Path, files: list[str]) -> list[dict[str, Any]]:
    leaks = []
    for rel in files:
        if any(rel.endswith(ext) for ext in (".tsx", ".jsx", ".html", ".vue")) and not (rel.startswith("tests/") or "node_modules" in rel):
            try:
                full_path = safe_path(root, rel)
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                matches = JARGON_PATTERN.findall(content)
                if matches:
                    leaks.append({"file": rel, "matches": sorted(list(set(matches)))})
            except Exception:
                pass
    return leaks


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

    # 1. Auditoria de Persistência
    db_files = [f for f in files if any(f.endswith(ext) for ext in (".db", ".sqlite", ".sqlite3"))]
    has_docker_db = False
    for f in files:
        if ("docker-compose" in f) and (f.endswith(".yml") or f.endswith(".yaml")):
            try:
                c = (root / f).read_text(encoding="utf-8", errors="ignore").lower()
                if any(k in c for k in ("postgres", "mysql", "mariadb", "mongo", "redis")):
                    has_docker_db = True
                    break
            except Exception:
                pass

    db_driver_found = False
    for f in files:
        if any(f.endswith(ext) for ext in (".csproj", "package.json", "requirements.txt", "pyproject.toml")):
            try:
                txt = (root / f).read_text(encoding="utf-8", errors="ignore").lower()
                if any(k in txt for k in ("npgsql", "entityframeworkcore", "dapper", "prisma", "typeorm", "psycopg", "sqlalchemy", "better-sqlite3", "pg")):
                    db_driver_found = True
                    break
            except Exception:
                pass

    persistence_status = "database_configured" if (db_files or has_docker_db or db_driver_found) else "in_memory_or_unconfigured"

    # 2. Auditoria de Autenticação e Criptografia
    has_auth_markers = False
    for f in files:
        if any(f.endswith(ext) for ext in (".cs", ".ts", ".js", ".py")) and not f.startswith("tests/"):
            try:
                txt = (root / f).read_text(encoding="utf-8", errors="ignore").lower()
                if any(k in txt for k in ("addauthentication", "jwtbearer", "bcrypt", "argon2", "passwordhasher", "jsonwebtoken", "passport")):
                    has_auth_markers = True
                    break
            except Exception:
                pass
    auth_status = "present" if has_auth_markers else "missing_or_unimplemented"

    # 3. Auditoria de Configurações e Segredos
    config_files = [f for f in files if any(f.endswith(name) for name in (".env", ".env.example", "appsettings.json", "appsettings.Development.json", "config.yaml"))]

    # 4. Auditoria de Jargão Técnico na UI
    jargon_leaks = find_ui_jargon_leaks(root, files)

    return {
        "project_root": str(root),
        "file_count_listed": len(files),
        "truncated": len(files) >= 5000,
        "stack_markers": stacks,
        "architecture_audit": {
            "persistence_status": persistence_status,
            "persistence_details": {
                "db_files_found": db_files,
                "has_docker_db": has_docker_db,
                "db_driver_found": db_driver_found
            },
            "auth_status": auth_status,
            "config_files": config_files,
            "ui_tech_jargon_leaks": jargon_leaks
        },
        "files": files
    }


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
            extra = ROLE_EXTRA_SECTIONS.get(agent, "")
            content = f"# {agent.replace('_', ' ').title()} — Relatório\n\n- **Status:** PLANEJADO\n- **Atualizado em:** {date.today().isoformat()}\n- **Demanda/roadmap:** [preencher]\n- **Responsabilidade:** {agent}\n\n" + extra + BASE_SECTIONS
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
    base_required_sections = ["Contexto e evidências", "O que precisa ser feito", "Plano", "O que foi feito", "Validação", "Pendências"]
    evidence_links = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    issues: list[str] = []

    # Localiza arquivos do projeto para verificar jargões
    ignored = {".git", ".agents", "node_modules", ".venv", "bin", "obj"}
    proj_files: list[str] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(names):
            proj_files.append(Path(current, name).relative_to(root).as_posix())

    ui_jargon_leaks = find_ui_jargon_leaks(root, proj_files)
    for leak in ui_jargon_leaks:
        issues.append(f"Vazamento de Jargão Técnico na UI ({leak['file']}): termos detectados {leak['matches']}")

    for rel in required:
        path = safe_path(root, rel)
        exists = path.is_file()
        content = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        
        # Identifica se é relatório de agente
        agent_key = next((k for k, v in AGENTS.items() if f".agentes/{v}" == rel), None)
        
        sections_missing = []
        if agent_key:
            req_headings = list(base_required_sections)
            if agent_key in ROLE_REQUIRED_HEADINGS:
                req_headings.extend(ROLE_REQUIRED_HEADINGS[agent_key])
            sections_missing = [heading for heading in req_headings if f"## {heading}" not in content]

        # Auditoria de integridade de links
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

        # Regra de Persistência Transparente para o DBA
        if agent_key == "dba" and re.search(r'status:\s*\**\s*conclu[ií]do', content, re.IGNORECASE):
            upper_content = content.upper()
            if ("EM MEMÓRIA" in upper_content or "EM MEMORIA" in upper_content or "LIST<" in upper_content) and ("POSTGRES" not in upper_content and "SQLITE" not in upper_content and "MIGRATIONS" not in upper_content):
                issues.append("Gap de Persistência em dba.md: Não é permitido aprovar como CONCLUÍDO enquanto o armazenamento for puramente em memória List<T>.")

        result = {"path": rel, "exists": exists, "non_empty": bool(content.strip()),
                  "missing_sections": sections_missing, "broken_local_links": broken_links,
                  "has_validation_evidence_section": "Validação" in content or "ValidaÃ§Ã£o" in content}
        results.append(result)
        if not exists or not content.strip():
            issues.append(f"Ausente ou vazio: {rel}")
        if sections_missing:
            issues.append(f"Seções obrigatórias ausentes em {rel}: {', '.join(sections_missing)}")
        if broken_links:
            issues.append(f"Links locais sem evidência em {rel}: {', '.join(broken_links)}")

    return {"valid": not issues, "issues": issues, "artifacts": results, "ui_jargon_leaks_count": len(ui_jargon_leaks)}


TOOLS = [
    {"name": "inspect_project", "description": "Lista arquivos do projeto-alvo, detecta stacks, audita persistência (DB), autenticação/criptografia, configs e vazamento de jargões na UI.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "initialize_squad_docs", "description": "Cria .agentes com índice, relatórios especializados com seções profundas de integração e persistência, roadmap e mapa.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "update_agent_report", "description": "Cria ou substitui o relatório completo de um agente em .agentes/.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "agent": {"type": "string", "enum": list(AGENTS)}, "content": {"type": "string"}}, "required": ["project_root", "agent", "content"]}},
    {"name": "update_roadmap", "description": "Cria ou substitui .agentes/coordenacao/roadmap.md.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "content": {"type": "string"}}, "required": ["project_root", "content"]}},
    {"name": "validate_squad_artifacts", "description": "Verifica existência, seções especializadas, links de evidência, transparência de persistência do DBA e vazamento de jargão na UI.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
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
                "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "antigravity-squad", "version": "1.1.0"}}}
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
