#!/usr/bin/env python3
"""Small, dependency-free MCP stdio server for Antigravity Squad artifacts, architecture auditing and adversarial code review."""
from __future__ import annotations

import json
import os
import re
import subprocess
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
    "code_critic_blind": "qualidade/critica-cega-codigo.md",
    "code_critic_spec": "qualidade/critica-especificacao-roadmap.md",
    "finalizer": "qualidade/finalizer.md",
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

[Mapeamento das APIs oficiais de marketplaces (Mercado Livre Developers, Shopee Open Platform, Amazon Creator PA-API, TikTok Shop Partner) e WhatsApp Business Cloud API oficial da Meta.]

## Gestão de Credenciais e Configurações

[Especificação da tela/módulo de Conexões onde o usuário cadastra chaves de API, webhooks e tokens com segurança.]
""",
    "dba": """## Mecanismo de Persistência Físico

[Onde e como os dados residem fisicamente (PostgreSQL 17, SQLite, etc.). Não aprovar persistência puramente em memória List<T> como concluída.]
""",
    "appsec": """## Autenticação e Criptografia

[Fluxo de login/sessão, hashing seguro de senhas (BCrypt, Argon2, PBKDF2), proteção de tokens e criptografia de credenciais de terceiros.]

## Testes de Segurança e PoCs

[Provas de conceito de ataque simulado (Red Team) e evidência de testes automatizados de segurança (Blue Team) cobrindo autorização em rotas de mutação, SSRF e proteção de segredos.]
""",
    "frontend": """## Linguagem do Usuário e Anti-Jargão

[Garantia de que a interface não exibe termos técnicos, badges de framework (.NET, React, etc.) ou jargões de backend.]
""",
    "designer": """## Linguagem do Usuário e Anti-Jargão

[Vocabulário estritamente voltado ao domínio de negócio e à jornada do usuário, eliminando tech-jargon e métricas falsas.]
""",
    "code_critic_blind": """## Veredito do Auditor Cego (Adversarial)

[APROVADO ou REPROVADO com base na análise fria do diff e código-fonte, sem contaminação de contexto.]

## Violações de Qualidade e Anti-Patterns Detectados

[Apontamento implacável de mocks, fake data, fake metrics, timers simulados, falhas de persistência ou segurança.]

## Pontos para Confronto com o Auditor de Requisitos

[Dúvidas e questionamentos técnicos a serem debatidos com o auditor de especificação.]
""",
    "code_critic_spec": """## Veredito do Auditor de Requisitos

[APROVADO ou REPROVADO quanto à fidelidade ao roadmap.md e pesquisa do PM.]

## Aderência ao Roadmap e PRD

[Checagem item a item se o que foi entregue atende aos critérios de aceite ou se atalhos foram tomados.]

## Síntese do Debate com o Auditor Cego

[Confronto entre as exigências técnicas do auditor cego e a viabilidade do escopo contratado.]
""",
}

ROLE_REQUIRED_HEADINGS = {
    "pm": ["Pesquisa de APIs e Integrações", "Gestão de Credenciais e Configurações"],
    "dba": ["Mecanismo de Persistência Físico"],
    "appsec": ["Autenticação e Criptografia", "Testes de Segurança e PoCs"],
    "frontend": ["Linguagem do Usuário e Anti-Jargão"],
    "designer": ["Linguagem do Usuário e Anti-Jargão"],
    "code_critic_blind": ["Veredito do Auditor Cego (Adversarial)", "Violações de Qualidade e Anti-Patterns Detectados"],
    "code_critic_spec": ["Veredito do Auditor de Requisitos", "Aderência ao Roadmap e PRD"],
    "finalizer": ["Checklist de conclusÃ£o", "Veredito final", "PendÃªncias bloqueantes"],
}

FINALIZER_CHECKS = [
    "InventÃ¡rio real de projetos e existÃªncia de client separado",
    "IntegraÃ§Ã£o browser/frontend com endpoints reais do backend",
    "ConexÃ£o e inicializaÃ§Ã£o do banco local",
    "Connection string e acesso pelo Visual Studio quando aplicÃ¡vel",
    "Migrations ou schema",
    "Logs locais e tratamento de exceÃ§Ãµes",
    "Build",
    "Testes unitÃ¡rios",
    "Testes de integraÃ§Ã£o",
    "Fluxos principais no browser",
]

ROLE_REQUIRED_HEADINGS["finalizer"] = ["Checklist de conclus\u00e3o", "Veredito final", "Pend\u00eancias bloqueantes"]
FINALIZER_CHECKS = [
    "Invent\u00e1rio real de projetos e exist\u00eancia de client separado",
    "Integra\u00e7\u00e3o browser/frontend com endpoints reais do backend",
    "Conex\u00e3o e inicializa\u00e7\u00e3o do banco local",
    "Connection string e acesso pelo Visual Studio quando aplic\u00e1vel",
    "Migrations ou schema",
    "Logs locais e tratamento de exce\u00e7\u00f5es",
    "Build",
    "Testes unit\u00e1rios",
    "Testes de integra\u00e7\u00e3o",
    "Fluxos principais no browser",
]

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


def get_docs_dir(root: Path) -> str:
    """Retorna .squad como padrão; preserva .agentes apenas se já existir e .squad não."""
    if (root / ".squad").is_dir():
        return ".squad"
    if (root / ".agentes").is_dir():
        return ".agentes"
    return ".squad"


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
    docs_dir = get_docs_dir(root)
    ignored = {".git", ".agents", ".agentes", ".squad", "node_modules", ".venv", "bin", "obj", "dist", "build", ".next", ".output"}
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

    # 4. Auditoria de .gitignore para a pasta de documentação
    gitignore_path = root / ".gitignore"
    gitignore_has_docs = False
    if gitignore_path.exists():
        gi_txt = gitignore_path.read_text(encoding="utf-8", errors="ignore")
        gitignore_has_docs = (f"{docs_dir}/" in gi_txt) or (docs_dir in gi_txt.splitlines())

    # 5. Auditoria de Jargão Técnico na UI
    jargon_leaks = find_ui_jargon_leaks(root, files)
    integration_test_paths = []
    for f in files:
        if "test" not in f.lower() or not f.lower().endswith((".cs", ".ts", ".js", ".py")):
            continue
        try:
            test_text = safe_path(root, f).read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?i)integration|webapplicationfactory|testcontainer|testserver|httpclient", f + "\n" + test_text):
                integration_test_paths.append(f)
        except Exception:
            pass

    return {
        "project_root": str(root),
        "docs_dir": docs_dir,
        "file_count_listed": len(files),
        "truncated": len(files) >= 5000,
        "stack_markers": stacks,
        "project_inventory": {
            "solution_files": [f for f in files if Path(f).suffix.lower() in (".sln", ".slnx")],
            "dotnet_projects": [f for f in files if f.lower().endswith(".csproj")],
            "package_manifests": [f for f in files if Path(f).name == "package.json"],
            "client_projects": [f for f in files if Path(f).name == "package.json" and any(part in f.lower().split("/") for part in ("client", "frontend", "web", "ui"))],
            "embedded_ui": [f for f in files if re.search(r"(^|/)wwwroot/index\.html$", f, re.IGNORECASE)],
            "migration_or_schema_files": [f for f in files if re.search(r"(^|/)(migrations?|schema)(/|\.)|\.sql$", f, re.IGNORECASE)],
            "test_projects": [f for f in files if "test" in Path(f).name.lower() and f.lower().endswith((".csproj", "package.json", "pyproject.toml"))],
            "integration_test_paths": integration_test_paths,
            "local_log_files": [f for f in files if f.lower().endswith((".log", ".log.1"))],
        },
        "architecture_audit": {
            "persistence_status": persistence_status,
            "persistence_details": {
                "db_files_found": db_files,
                "has_docker_db": has_docker_db,
                "db_driver_found": db_driver_found
            },
            "auth_status": auth_status,
            "config_files": config_files,
            "gitignore_has_docs": gitignore_has_docs,
            "ui_tech_jargon_leaks": jargon_leaks
        },
        "files": files
    }


def audit_code_delivery(args: dict[str, Any]) -> dict[str, Any]:
    """Ferramenta mecânica para os Críticos de Código: audita armadilhas, mocks, timers e fake metrics."""
    root = project_root(args.get("project_root", ""))
    ignored = {".git", ".agents", ".agentes", ".squad", "node_modules", ".venv", "bin", "obj", "dist", "build", ".next", ".output"}
    files: list[str] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(names):
            files.append(Path(current, name).relative_to(root).as_posix())

    findings: list[str] = []

    # 1. Vazamento de jargão de dev
    jargon_leaks = find_ui_jargon_leaks(root, files)
    for leak in jargon_leaks:
        findings.append(f"Vazamento de Jargão Técnico na UI ({leak['file']}): {leak['matches']}")

    # 2. Trapaças no Frontend: timers simulando rede, random IDs, métricas inventadas, mocks camuflados
    timer_pattern = re.compile(r'setIs\w+\(true\)[^;]*;\s*setTimeout|setTimeout\s*\(\s*\(\)\s*=>\s*\{[^}]*set(?:Offers|Links|Converted|Products|Data)', re.DOTALL | re.IGNORECASE)
    random_id_pattern = re.compile(r'Math\.random\(\)\.toString\(36\)', re.IGNORECASE)
    fake_metrics_pattern = re.compile(r'(?:1[,.]248|24[,.]590|R\$\s*3[,.]840)', re.IGNORECASE)
    mock_data_pattern = re.compile(r'(?:const|let|var)\s+(?:FALLBACK_\w*|MOCK_\w*|mockData|mockOffers|dummyItems|fakeProducts|sampleDeals)\b', re.IGNORECASE)

    for f in files:
        if any(f.endswith(ext) for ext in (".tsx", ".jsx", ".ts", ".js")) and not (f.startswith("tests/") or "node_modules" in f):
            try:
                full_path = safe_path(root, f)
                txt = full_path.read_text(encoding="utf-8", errors="ignore")
                if timer_pattern.search(txt):
                    findings.append(f"Latência Simulada (setTimeout) em {f}. Proibido simular atraso de rede.")
                if random_id_pattern.search(txt):
                    findings.append(f"Geração Falsa de IDs (Math.random) em {f}. IDs devem vir do backend.")
                if fake_metrics_pattern.search(txt):
                    findings.append(f"Métricas Inventadas (Fake Metrics) em {f}. Remova números fictícios da interface.")
                if mock_data_pattern.search(txt):
                    findings.append(f"Dados em Mock Camuflados (Mock/Fallback Array) em {f}. Proibido embutir dados fictícios; o frontend deve renderizar estado vazio ou consumir a API real.")
            except Exception:
                pass

    # 3. Trapaças no Backend: empty catch, Thread.Sleep
    empty_catch_pattern = re.compile(r'catch\s*\([^\)]*\)\s*\{\s*\}', re.IGNORECASE)
    for f in files:
        if f.endswith(".cs") or f.endswith(".go") or f.endswith(".py"):
            try:
                full_path = safe_path(root, f)
                txt = full_path.read_text(encoding="utf-8", errors="ignore")
                if empty_catch_pattern.search(txt):
                    findings.append(f"Tratamento Vazio de Erro (empty catch) em {f}.")
                if "Thread.Sleep" in txt:
                    findings.append(f"Bloqueio síncrono (Thread.Sleep) em {f}.")
            except Exception:
                pass

    verdict = "APROVADO" if not findings else "REPROVADO"
    return {
        "project_root": str(root),
        "verdict": verdict,
        "clean": not findings,
        "findings_count": len(findings),
        "findings": findings
    }


def audit_security_controls(args: dict[str, Any]) -> dict[str, Any]:
    """Ferramenta mecânica do @AppSec: audita proteção de rotas críticas, testes de segurança automatizados e criptografia de credenciais."""
    root = project_root(args.get("project_root", ""))
    ignored = {".git", ".agents", ".agentes", ".squad", "node_modules", ".venv", "bin", "obj", "dist", "build", ".next", ".output"}
    files: list[str] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(names):
            files.append(Path(current, name).relative_to(root).as_posix())

    findings: list[str] = []
    security_tests_found: list[str] = []

    # 1. Checagem de Testes de Segurança Automatizados (AppSec)
    test_files = [f for f in files if "test" in f.lower() and any(f.endswith(ext) for ext in (".cs", ".ts", ".js", ".py"))]
    for tf in test_files:
        base_name = Path(tf).name.lower()
        if any(sec in base_name for sec in ("security", "ssrf", "auth", "bola", "idor", "xss", "csrf", "crypto")):
            security_tests_found.append(tf)

    if not security_tests_found:
        findings.append("Ausência de Testes de Segurança Automatizados (AppSec): Nenhum arquivo de teste contendo verificações de segurança (Security/SSRF/Auth/Crypto) encontrado em testes.")

    # 2. Checagem de Rotas Críticas e Mutação sem [Authorize]
    for f in files:
        if ("controller" in f.lower() or "routes" in f.lower() or "endpoint" in f.lower()) and f.endswith(".cs"):
            try:
                full_path = safe_path(root, f)
                txt = full_path.read_text(encoding="utf-8", errors="ignore")
                is_sensitive_controller = any(c in f.lower() for c in ("whatsapp", "integrations", "admin", "dispatch", "payment", "user"))
                if is_sensitive_controller:
                    has_class_authorize = bool(re.search(r'\[Authorize(?:Attribute)?\]', txt))
                    if not has_class_authorize:
                        sensitive_actions = re.findall(r'\[Http(?:Post|Put|Delete)[^\]]*\]\s*(?:\[[^\]]+\]\s*)*public\s+[^\(]+\s+(\w+)\s*\(', txt)
                        for action in sensitive_actions:
                            # Webhooks de marketplaces utilizam validação por assinatura HMAC em vez de token de usuário JWT
                            if "webhook" in action.lower():
                                continue
                            method_block = re.search(r'(\[[^\]]*Authorize[^\]]*\]\s*)+\[Http(?:Post|Put|Delete)[^\]]*\]\s*(?:\[[^\]]+\]\s*)*public\s+[^\(]+\s+' + re.escape(action), txt)
                            if not method_block:
                                findings.append(f"Rota Crítica Desprotegida: A ação '{action}' em {f} não possui o atributo [Authorize] obrigatório.")
            except Exception:
                pass

    # 3. Checagem de Criptografia de Credenciais de Terceiros (AppSec & DBA)
    credentials_encryption_status = "present"
    has_credentials_entity = False
    has_encryption_service = False

    for f in files:
        if any(f.endswith(ext) for ext in (".cs", ".ts", ".py")):
            try:
                full_path = safe_path(root, f)
                txt = full_path.read_text(encoding="utf-8", errors="ignore")
                if "PlatformIntegrationConfig" in txt or "IntegrationConfig" in txt or ("ApiKey" in txt and "ApiSecret" in txt):
                    has_credentials_entity = True
                if any(k in txt for k in ("Aes", "DataProtection", "EncryptionService", "EncryptString", "ProtectedPersonalData", "HMACSHA256")):
                    has_encryption_service = True
            except Exception:
                pass

    if has_credentials_entity and not has_encryption_service:
        credentials_encryption_status = "plaintext_vulnerable"
        findings.append("Risco de Armazenamento Inseguro: Entidade armazena ApiKey/ApiSecret/Tokens de terceiros sem serviço de criptografia detectado no projeto.")

    verdict = "APROVADO" if not findings else "REPROVADO"
    return {
        "project_root": str(root),
        "verdict": verdict,
        "clean": not findings,
        "findings_count": len(findings),
        "security_tests_found": security_tests_found,
        "credentials_encryption_status": credentials_encryption_status,
        "findings": findings
    }


def initialize_docs(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    docs_dir = get_docs_dir(root)
    docs = safe_path(root, docs_dir)
    docs.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    index = f"# Documentação do Antigravity Squad\n\nDemanda: [preencher]\n\n## Relatórios\n\n" + "".join(
        f"- [{name}](./{path})\n" for name, path in AGENTS.items()) + "\n## Roadmap\n\n- [Roadmap](./coordenacao/roadmap.md)\n"
    for relative in ["README.md", *AGENTS.values(), "coordenacao/roadmap.md", "PROJECT_MAP.md"]:
        target = safe_path(root, f"{docs_dir}/{relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        if relative == "README.md":
            content = index
        elif relative == "coordenacao/roadmap.md":
            content = "# Roadmap\n\n## Contexto e decisões\n\n[Contexto, stack observada e decisões.]\n\n## Itens\n\n[IDs, prioridade, status, escopo, dependências, critérios de aceite, validação e evidências.]\n"
        elif relative == "PROJECT_MAP.md":
            content = "# PROJECT_MAP — Índice confirmado do projeto\n\nConfirme caminhos e contratos antes de depender deste mapa.\n\n## Telas e componentes\n\n| Área | Caminho | Estados | Verificado em |\n|---|---|---|---|\n\n## Rotas e APIs\n\n| Fluxo | Método/rota | Contrato | Autorização | Evidência |\n|---|---|---|---|---|\n\n## Dados e integrações\n\n| Recurso | Fonte | Consumidores | Observações |\n|---|---|---|---|\n\n## Testes e operação\n\n| Escopo | Comando/documento | Resultado |\n|---|---|---|\n"
        elif relative == AGENTS["finalizer"]:
            headings = ROLE_REQUIRED_HEADINGS["finalizer"]
            rows = "".join(f"| {check} | [preencher] | [preencher] |\n" for check in FINALIZER_CHECKS)
            content = (f"# Finalizer - Relat\u00f3rio\n\n- **Status:** PLANEJADO\n- **Atualizado em:** {date.today().isoformat()}\n- **Demanda/roadmap:** [preencher]\n- **Responsabilidade:** auditoria final independente\n\n"
                       f"## {headings[0]}\n\nCada item deve ser `APROVADO`, `REPROVADO` ou `N/A`, com evid\u00eancia verific\u00e1vel. N/A exige motivo. Nos testes aprovados registre `Comando: ...; Resultado: ...`. Testes unit\u00e1rios n\u00e3o provam integra\u00e7\u00e3o. Relate interface embutida na API. LocalDB/Visual Studio s\u00f3 se aplica a .NET em Windows.\n\n"
                       "| Verifica\u00e7\u00e3o | Status | Evid\u00eancia (arquivo/rota; comando e resultado quando teste) |\n|---|---|---|\n" + rows +
                       f"\n## {headings[1]}\n\n**Veredito final:** [APROVADO ou REPROVADO]\n\n## {headings[2]}\n\n[Nenhuma, ou tarefas concretas vinculadas ao roadmap.]\n")
            content += "\n## Contexto e evid\u00eancias\n\n[A preencher.]\n\n## Decis\u00f5es e recomenda\u00e7\u00f5es\n\n[A preencher.]\n\n## O que precisa ser feito\n\n[A preencher.]\n\n## Plano e depend\u00eancias\n\n[A preencher.]\n\n## O que foi feito\n\n[A preencher.]\n\n## Valida\u00e7\u00e3o e evid\u00eancias\n\n[A preencher.]\n\n## Pend\u00eancias\n\n[A preencher.]\n\n## Fontes\n\n[A preencher.]\n"
        else:
            agent = next(k for k, v in AGENTS.items() if v == relative)
            extra = ROLE_EXTRA_SECTIONS.get(agent, "")
            content = f"# {agent.replace('_', ' ').title()} — Relatório\n\n- **Status:** PLANEJADO\n- **Atualizado em:** {date.today().isoformat()}\n- **Demanda/roadmap:** [preencher]\n- **Responsabilidade:** {agent}\n\n" + extra + BASE_SECTIONS
        target.write_text(content, encoding="utf-8", newline="\n")
        created.append(f"{docs_dir}/{relative}")

    # Garante automaticamente que a pasta de documentação esteja no .gitignore do projeto
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        gi_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
        if f"{docs_dir}/" not in gi_content and docs_dir not in gi_content.splitlines():
            with open(gitignore_path, "a", encoding="utf-8") as gf:
                if not gi_content.endswith("\n") and gi_content:
                    gf.write("\n")
                gf.write(f"\n# Antigravity Squad artifacts\n{docs_dir}/\n")
    else:
        gitignore_path.write_text(f"# Antigravity Squad artifacts\n{docs_dir}/\n", encoding="utf-8")

    return {"project_root": str(root), "docs_dir": docs_dir, "created": created, "preserved_existing": True}


def update_report(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    docs_dir = get_docs_dir(root)
    agent, content = args.get("agent"), args.get("content")
    if agent not in AGENTS:
        raise SquadError(f"agent deve ser um de: {', '.join(AGENTS)}")
    if not isinstance(content, str) or not content.strip():
        raise SquadError("content precisa conter o relatório completo")
    rel = f"{docs_dir}/{AGENTS[agent]}"
    target = safe_path(root, rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return {"updated": rel}


def update_roadmap(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    docs_dir = get_docs_dir(root)
    content = args.get("content")
    if not isinstance(content, str) or not content.strip():
        raise SquadError("content precisa conter o roadmap completo")
    rel = f"{docs_dir}/coordenacao/roadmap.md"
    target = safe_path(root, rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return {"updated": rel}


def _completion_declared(root: Path, docs_dir: str) -> bool:
    roadmap = safe_path(root, f"{docs_dir}/coordenacao/roadmap.md")
    if not roadmap.is_file():
        return False
    text = roadmap.read_text(encoding="utf-8", errors="replace")
    return bool(re.search(r"(?im)^\s*(?:[-*]|\|).*\b(?:CONCLU[IÃI]DO|VALIDADO)\b", text))


def _completion_declared(root: Path, docs_dir: str) -> bool:
    roadmap = safe_path(root, f"{docs_dir}/coordenacao/roadmap.md")
    if not roadmap.is_file():
        return False
    text = roadmap.read_text(encoding="utf-8", errors="replace")
    return bool(re.search(r"(?im)^\s*(?:[-*]|\|).*\b(?:CONCLU\w*|VALIDADO)\b", text))


def validate_completion_checklist(args: dict[str, Any]) -> dict[str, Any]:
    """Blocks final acceptance unless the independent finalizer has evidence for every gate."""
    root = project_root(args.get("project_root", ""))
    docs_dir = get_docs_dir(root)
    rel = f"{docs_dir}/{AGENTS['finalizer']}"
    path = safe_path(root, rel)
    content = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
    rows: dict[str, tuple[str, str]] = {}
    for line in content.splitlines():
        if not line.strip().startswith("|") or re.match(r"\|\s*:?-+", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            rows[cells[0].casefold()] = (cells[1].upper(), cells[2])

    results = []
    issues = []
    inspection = inspect_project({"project_root": str(root)})
    dotnet_windows = ".NET" in inspection["stack_markers"] and os.name == "nt"
    for required in FINALIZER_CHECKS:
        found = next((value for key, value in rows.items() if required.casefold() in key), None)
        status, evidence = found if found else ("AUSENTE", "")
        normalized = status.strip().upper()
        valid_status = normalized in ("APROVADO", "REPROVADO", "N/A", "NA", "NÃO APLICÁVEL", "NAO APLICAVEL")
        if required == FINALIZER_CHECKS[3] and not dotnet_windows:
            if normalized not in ("N/A", "NA", "NÃO APLICÁVEL", "NAO APLICAVEL"):
                issues.append(f"{required}: deve ser N/A fora de .NET/Windows.")
        elif normalized in ("N/A", "NA", "NÃO APLICÁVEL", "NAO APLICAVEL") and not re.search(r"(?i)(motivo|porque|por que|n/a porque)", evidence):
            issues.append(f"{required}: N/A precisa justificar a não aplicabilidade.")
        if not valid_status:
            issues.append(f"{required}: status ausente ou inválido.")
        if not evidence.strip() or re.search(r"(?i)\[(?:preencher|evid[eê]ncia|pendente)\]", evidence):
            issues.append(f"{required}: evidência ausente ou placeholder.")
        if normalized == "REPROVADO":
            issues.append(f"{required}: reprovado bloqueia o aceite final.")
        if required in (FINALIZER_CHECKS[6], FINALIZER_CHECKS[7], FINALIZER_CHECKS[8], FINALIZER_CHECKS[9]) and normalized == "APROVADO":
            if not re.search(r"(?i)(comando|command)\s*[:=].+", evidence) or not re.search(r"(?i)(resultado|result)\s*[:=].+", evidence):
                issues.append(f"{required}: aprovação exige comando e resultado explícitos.")
        if required == FINALIZER_CHECKS[8] and normalized == "APROVADO" and not re.search(r"(?i)(integra[cç][aã]o|integration|webapplicationfactory|testcontainer|teste de API)", evidence):
            issues.append("Testes de integração: evidência precisa identificar teste de integração/API; teste unitário não serve como prova.")
        if required == FINALIZER_CHECKS[1] and normalized == "APROVADO" and not re.search(r"(?i)(browser|navegador).*(request|requis)|request.*(?:HTTP\s*[2-5]\d\d|status\s*[2-5]\d\d)", evidence):
            issues.append("Browser/backend approval requires an actual browser request and observed HTTP status.")
        if required == FINALIZER_CHECKS[3] and normalized == "APROVADO" and dotnet_windows and not re.search(r"(?i)(localdb|visual studio).*(connection|string)|(connection|string).*(localdb|visual studio)", evidence):
            issues.append("Visual Studio/LocalDB approval requires evidence of configured connection string and access.")
        if required == FINALIZER_CHECKS[0] and normalized == "APROVADO":
            inventory = inspection["project_inventory"]
            listed_projects = [*inventory["solution_files"], *inventory["dotnet_projects"], *inventory["package_manifests"]]
            missing_projects = [project for project in listed_projects if project not in evidence]
            missing_ui = [ui for ui in inventory["embedded_ui"] if ui not in evidence]
            if missing_projects or missing_ui:
                issues.append(f"Project inventory evidence omits detected paths: {missing_projects + missing_ui}.")
        if required == FINALIZER_CHECKS[8] and normalized == "APROVADO":
            integration_paths = inspection["project_inventory"]["integration_test_paths"]
            if not integration_paths or not any(path in evidence for path in integration_paths):
                issues.append("Integration approval requires a detected integration test path and command/result for that test.")
        results.append({"check": required, "status": normalized, "evidence": evidence, "valid": not any(required in issue for issue in issues)})

    verdict_match = re.search(r"(?im)^\s*[-*]?\s*\*\*?veredito final\*\*?\s*:\s*(APROVADO|REPROVADO)\b", content)
    if not verdict_match or verdict_match.group(1).upper() != "APROVADO":
        issues.append("Veredito final precisa ser explicitamente APROVADO.")
    return {"valid": not issues, "blocks_final_acceptance": bool(issues), "checklist": results, "issues": issues,
            "project_inventory": inspection["project_inventory"], "platform_applicability": {"dotnet_windows": dotnet_windows}}


def validate_artifacts(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    docs_dir = get_docs_dir(root)
    required = [f"{docs_dir}/README.md", f"{docs_dir}/coordenacao/roadmap.md",
                *[f"{docs_dir}/{p}" for p in AGENTS.values()]]
    results = []
    base_required_sections = ["Contexto e evidências", "O que precisa ser feito", "Plano", "O que foi feito", "Validação", "Pendências"]
    evidence_links = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    issues: list[str] = []

    # Localiza arquivos do projeto para verificar jargões
    ignored = {".git", ".agents", ".agentes", ".squad", "node_modules", ".venv", "bin", "obj", "dist", "build", ".next", ".output"}
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
        agent_key = next((k for k, v in AGENTS.items() if f"{docs_dir}/{v}" == rel), None)

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

    # Validação mandatória de .gitignore para a pasta de documentação
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        gi_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
        if f"{docs_dir}/" not in gi_content and docs_dir not in gi_content.splitlines():
            issues.append(f"Aviso de Git: A pasta '{docs_dir}/' não está no .gitignore. Adicione '{docs_dir}/' ao .gitignore do projeto.")
    else:
        issues.append(f"Aviso de Git: Arquivo .gitignore ausente. Crie um .gitignore contendo '{docs_dir}/'.")

    completion_gate = None
    if _completion_declared(root, docs_dir):
        completion_gate = validate_completion_checklist(args)
        if not completion_gate["valid"]:
            issues.extend(f"Gate de conclusÃ£o: {issue}" for issue in completion_gate["issues"])
    return {"valid": not issues, "issues": issues, "artifacts": results, "ui_jargon_leaks_count": len(ui_jargon_leaks), "docs_dir": docs_dir,
            "completion_declared": _completion_declared(root, docs_dir), "completion_gate": completion_gate}


def get_skills_dir() -> Path:
    base = Path(__file__).resolve().parent.parent / "skills"
    if base.is_dir():
        return base
    canonical = Path("D:/Agentes/.antigravity/skills")
    if canonical.is_dir():
        return canonical
    user_skills = Path.home() / ".gemini" / "antigravity-cli" / "skills"
    if user_skills.is_dir():
        return user_skills
    return base


def get_design_reference(args: dict[str, Any]) -> dict[str, Any]:
    company = (args.get("company") or "").strip().lower()
    query = (args.get("query") or "").strip().lower()
    skills_dir = get_skills_dir()
    catalog_dir = skills_dir / "design-reference" / "design-md"

    if not catalog_dir.is_dir():
        return {"error": f"Diretório de design-md não encontrado em {catalog_dir}"}

    all_companies = sorted([d.name for d in catalog_dir.iterdir() if d.is_dir()])

    if not company and not query:
        return {
            "total_companies": len(all_companies),
            "companies": all_companies,
            "message": "Passe 'company' (ex: 'linear', 'stripe', 'vercel', 'supabase') para obter o contrato completo, ou 'query' para pesquisar padrões."
        }

    if company:
        matched_dir = None
        company_name = company
        for c in all_companies:
            if c.lower() == company or c.lower().startswith(company) or company in c.lower():
                matched_dir = catalog_dir / c
                company_name = c
                break

        if not matched_dir or not matched_dir.is_dir():
            suggestions = [c for c in all_companies if (len(company) >= 2 and company[:2] in c.lower())][:8]
            return {
                "error": f"Empresa '{company}' não encontrada no catálogo de referências.",
                "suggestions": suggestions
            }

        design_file = matched_dir / "DESIGN.md"
        readme_file = matched_dir / "README.md"
        content = ""
        file_used = design_file
        if design_file.is_file():
            content = design_file.read_text(encoding="utf-8", errors="replace")
        elif readme_file.is_file():
            file_used = readme_file
            content = readme_file.read_text(encoding="utf-8", errors="replace")

        return {
            "company": company_name,
            "file": file_used.name,
            "content": content
        }

    matches = []
    for c in all_companies:
        c_dir = catalog_dir / c
        d_file = c_dir / "DESIGN.md"
        if not d_file.is_file():
            d_file = c_dir / "README.md"
            if not d_file.is_file():
                continue
        text = d_file.read_text(encoding="utf-8", errors="replace")
        if query in text.lower():
            lines = text.splitlines()
            matching_lines = []
            for i, line in enumerate(lines):
                if query in line.lower():
                    start = max(0, i - 1)
                    end = min(len(lines), i + 3)
                    matching_lines.append("\n".join(lines[start:end]))
                    if len(matching_lines) >= 2:
                        break
            matches.append({
                "company": c,
                "snippets": matching_lines
            })

    return {
        "query": query,
        "matched_count": len(matches),
        "results": matches[:15]
    }


def audit_frontend_taste(args: dict[str, Any]) -> dict[str, Any]:
    root = project_root(args.get("project_root", ""))
    ignored = {".git", ".agents", ".agentes", ".squad", "node_modules", ".venv", "bin", "obj", "dist", "build", ".next", ".output"}

    ai_cliches = [
        "unlock your potential", "unlock the power", "supercharge your", "game-changing", "game changer",
        "next-generation", "next-gen", "cutting-edge", "seamless integration", "dive deep into",
        "elevate your", "revolutionize", "discover the power", "in today's fast-paced world",
        "trusted by over", "trusted by fortune 500", "loved by 10,000+"
    ]

    hardcoded_hex_regex = re.compile(r'(?:bg|text|border|fill|stroke)-\[#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\]')
    arbitrary_px_regex = re.compile(r'(?:p|px|py|m|mx|my|w|h|gap)-\[\d{2,}px\]')

    frontend_extensions = {".tsx", ".jsx", ".html", ".vue", ".svelte", ".astro"}
    files_audited = 0
    issues: list[dict[str, Any]] = []

    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ignored)
        for name in sorted(names):
            p = Path(current, name)
            if p.suffix.lower() not in frontend_extensions:
                continue
            files_audited += 1
            rel_file = p.relative_to(root).as_posix()
            try:
                content = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            content_lower = content.lower()

            for cliche in ai_cliches:
                if cliche in content_lower:
                    issues.append({
                        "file": rel_file,
                        "type": "ai_copy_cliche",
                        "severity": "medium",
                        "match": cliche,
                        "message": f"Clichê de IA / marketing genérico detectado ('{cliche}'). Substitua por linguagem de domínio concisa e direta."
                    })

            hex_matches = hardcoded_hex_regex.findall(content)
            if hex_matches:
                issues.append({
                    "file": rel_file,
                    "type": "hardcoded_hex_token",
                    "severity": "low",
                    "matches": list(set(hex_matches))[:5],
                    "count": len(hex_matches),
                    "message": "Cores hexadecimais arbitrárias em classes Tailwind. Recomenda-se usar tokens semânticos (ex: primary, accent, muted, card, border)."
                })

            px_matches = arbitrary_px_regex.findall(content)
            if len(px_matches) > 3:
                issues.append({
                    "file": rel_file,
                    "type": "arbitrary_spacing_dimensions",
                    "severity": "low",
                    "matches": list(set(px_matches))[:5],
                    "message": "Múltiplos espaçamentos arbitrários em pixels. Use a escala consistente de espaçamento do design system (Tailwind)."
                })

            if ("animate-" in content or "transition-" in content) and "motion-reduce" not in content and "prefers-reduced-motion" not in content:
                if content.count("animate-") > 2:
                    issues.append({
                        "file": rel_file,
                        "type": "missing_reduced_motion",
                        "severity": "medium",
                        "message": "Animações ativas sem tratamento para 'motion-reduce:transition-none' ou 'motion-reduce:animate-none' (Acessibilidade WCAG)."
                    })

    score = max(0, 100 - (len(issues) * 10))
    passed = len([i for i in issues if i["severity"] in ("high", "medium")]) == 0

    return {
        "project_root": str(root),
        "files_audited": files_audited,
        "taste_score": score,
        "passed": passed,
        "total_issues": len(issues),
        "issues": issues,
        "recommendations": [
            "Use tokens semânticos (bg-primary, text-muted-foreground) em vez de classes hexadecimais arbitrárias.",
            "Elimine textos clichês de IA e adote vocabulário prático focado nas tarefas reais do usuário.",
            "Garanta suporte a 'prefers-reduced-motion' para acessibilidade."
        ]
    }


def run_playwright_cli(args: dict[str, Any]) -> dict[str, Any]:
    cmd = (args.get("command") or "snapshot").strip().lower()
    url = (args.get("url") or "").strip()
    viewport = (args.get("viewport") or "desktop").strip().lower()
    proj_root_arg = args.get("project_root")
    output_path = args.get("output_path")

    skills_dir = get_skills_dir()
    playwright_script = skills_dir / "playwright-cli" / "playwright-cli.js"

    if not playwright_script.is_file():
        playwright_script = Path("D:/Agentes/.antigravity/skills/playwright-cli/playwright-cli.js")

    if not playwright_script.is_file():
        raise SquadError(f"playwright-cli.js não encontrado em {playwright_script}")

    cli_args = ["node", str(playwright_script)]

    if cmd == "open":
        if not url:
            raise SquadError("Comando 'open' requer o argumento 'url'")
        cli_args.extend(["open", url])
    elif cmd == "close":
        cli_args.append("close")
    elif cmd == "snapshot":
        cli_args.append("snapshot")
    elif cmd == "console":
        cli_args.append("console")
    elif cmd == "requests":
        cli_args.append("requests")
    elif cmd == "resize":
        if viewport == "mobile":
            cli_args.extend(["resize", "390", "844"])
        elif viewport == "desktop":
            cli_args.extend(["resize", "1440", "900"])
        elif "x" in viewport:
            parts = viewport.split("x")
            cli_args.extend(["resize", parts[0], parts[1]])
        else:
            cli_args.extend(["resize", "1440", "900"])
    elif cmd == "screenshot":
        cli_args.append("screenshot")
        if output_path:
            cli_args.extend(["--filename", output_path])
        elif proj_root_arg:
            root = project_root(proj_root_arg)
            docs_dir = get_docs_dir(root)
            evid_dir = root / docs_dir / "evidencias" / "frontend"
            evid_dir.mkdir(parents=True, exist_ok=True)
            shot_file = evid_dir / f"screenshot_{viewport}_{date.today().isoformat()}.png"
            cli_args.extend(["--filename", str(shot_file)])
            output_path = str(shot_file)
    else:
        cli_args.append(cmd)
        if url:
            cli_args.append(url)

    try:
        proc = subprocess.run(cli_args, capture_output=True, text=True, timeout=30)
        return {
            "command": cmd,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "output_path": output_path,
            "success": proc.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"command": cmd, "success": False, "error": "Timeout de 30s ao executar playwright-cli"}
    except Exception as exc:
        return {"command": cmd, "success": False, "error": str(exc)}


TOOLS = [
    {"name": "validate_completion_checklist", "description": "Valida o aceite do agente finalizador independente. Requer status e evid\u00eancia em cada gate e bloqueia lacunas, reprova\u00e7\u00f5es ou testes sem comando/resultado.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "inspect_project", "description": "Lista arquivos, detecta stacks, audita persistência (DB), autenticação/criptografia, configs e vazamento de jargões na UI.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "audit_code_delivery", "description": "Audita mecanicamente o código-fonte contra trapaças: setTimeout, Math.random fake IDs, fake metrics, empty catch e jargões na UI.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "initialize_squad_docs", "description": "Cria .squad com índice, relatórios especializados, seções profundas de integração, os dois críticos, roadmap e mapa.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "update_agent_report", "description": "Cria ou substitui o relatório completo de um agente em .squad/.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "agent": {"type": "string", "enum": list(AGENTS)}, "content": {"type": "string"}}, "required": ["project_root", "agent", "content"]}},
    {"name": "update_roadmap", "description": "Cria ou substitui .squad/coordenacao/roadmap.md.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}, "content": {"type": "string"}}, "required": ["project_root", "content"]}},
    {"name": "validate_squad_artifacts", "description": "Verifica existência, seções especializadas, links de evidência, transparência de persistência do DBA e vazamento de jargão na UI.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "audit_security_controls", "description": "Audita mecanismos de segurança do AppSec: proteção de rotas com autenticação/JWT, testes de segurança automatizados (SSRF, Auth, BOLA) e criptografia de credenciais de terceiros.", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string"}}, "required": ["project_root"]}},
    {"name": "get_design_reference", "description": "Consulta o catálogo de 84 sistemas de design de classe mundial (Linear, Stripe, Vercel, Supabase, Apple, etc.) do awesome-design-md ou pesquisa padrões visuais.", "inputSchema": {"type": "object", "properties": {"company": {"type": "string", "description": "Nome da empresa de referência (ex: 'linear', 'stripe', 'vercel', 'supabase', 'apple', 'airbnb')"}, "query": {"type": "string", "description": "Termo de busca livre nos DESIGN.md (ex: 'dark mode', 'tokens', 'spacing')"}}}},
    {"name": "audit_frontend_taste", "description": "Audita a interface do usuário contra AI slop e clichês de design (heurísticas taste-skill: cópia genérica, cores hex não padronizadas, falta de reduced-motion).", "inputSchema": {"type": "object", "properties": {"project_root": {"type": "string", "description": "Raiz do projeto a auditar"}}, "required": ["project_root"]}},
    {"name": "run_playwright_cli", "description": "Executa comandos do Microsoft Playwright CLI integrado (screenshot, snapshot, console, requests, resize, open, close) para capturar evidências reais do navegador.", "inputSchema": {"type": "object", "properties": {"command": {"type": "string", "enum": ["open", "snapshot", "screenshot", "console", "requests", "resize", "close"], "description": "Comando Playwright a executar"}, "url": {"type": "string", "description": "URL da aplicação (ex: http://localhost:5173)"}, "viewport": {"type": "string", "enum": ["desktop", "mobile"], "description": "Tamanho da viewport (desktop: 1440x900, mobile: 390x844)"}, "project_root": {"type": "string", "description": "Raiz do projeto"}, "output_path": {"type": "string", "description": "Caminho explícito de destino para captura/screenshot"}}, "required": ["command"]}},
]
HANDLERS = {"inspect_project": inspect_project, "audit_code_delivery": audit_code_delivery,
            "validate_completion_checklist": validate_completion_checklist,
            "initialize_squad_docs": initialize_docs, "update_agent_report": update_report,
            "update_roadmap": update_roadmap, "validate_squad_artifacts": validate_artifacts,
            "audit_security_controls": audit_security_controls,
            "get_design_reference": get_design_reference,
            "audit_frontend_taste": audit_frontend_taste,
            "run_playwright_cli": run_playwright_cli}


def respond(message: dict[str, Any]) -> dict[str, Any] | None:
    method, ident, params = message.get("method"), message.get("id"), message.get("params", {})
    if method == "notifications/initialized" or method == "notifications/cancelled":
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": ident, "result": {"protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": "antigravity-squad", "version": "1.3.0"}}}
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
        line_clean = line.strip().lstrip("\ufeff")
        if not line_clean:
            continue
        try:
            result = respond(json.loads(line_clean))
            if result is not None:
                sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
