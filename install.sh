#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/.antigravity"
kinds=(agents rules skills commands mcp)

if [[ ! -d "$source_dir" ]]; then
  echo "Erro: pasta fonte .antigravity não encontrada em $script_dir" >&2
  exit 1
fi

copy_squad_to() {
  local destination_root="$1"
  mkdir -p "$destination_root"
  for kind in "${kinds[@]}"; do
    if [[ -d "$source_dir/$kind" ]]; then
      mkdir -p "$destination_root/$kind"
      cp -R "$source_dir/$kind/." "$destination_root/$kind/"
    fi
  done
  local skill_dir="$destination_root/skills/antigravity-squad"
  mkdir -p "$skill_dir/templates"
  cp "$source_dir/skills/antigravity-squad/SKILL.md" "$skill_dir/"
  cp -R "$source_dir/skills/antigravity-squad/templates/." "$skill_dir/templates/"
}

install_global() {
  local config_dir="$HOME/.gemini/config"
  copy_squad_to "$config_dir"
  local global_skills_dir="$HOME/.gemini/antigravity-cli/skills"
  mkdir -p "$global_skills_dir"
  cp -R "$source_dir/skills/." "$global_skills_dir/"
  echo "Squad e skills instalados globalmente em $config_dir e $global_skills_dir"
  echo "MCP server: python3 '$config_dir/mcp/server.py' (stdio)"
}

if [[ "${1:-}" == "--global" || "${1:-}" == "-g" ]]; then
  install_global
  exit 0
fi

target_project="${1:-}"
if [[ -z "$target_project" ]]; then
  echo "1) Instalar no diretório atual ($(pwd))"
  echo "2) Informar outro projeto"
  echo "3) Instalar globalmente"
  echo "q) Cancelar"
  read -rp "Opção: " choice
  case "$choice" in
    1) target_project="$(pwd)" ;;
    2) read -rp "Raiz do projeto: " target_project ;;
    3) install_global; exit 0 ;;
    *) echo "Cancelado."; exit 0 ;;
  esac
fi

if [[ ! -d "$target_project" ]]; then
  echo "Diretório de projeto não encontrado: $target_project" >&2
  exit 1
fi
copy_squad_to "$target_project/.agents"

# Garante .squad/ no .gitignore do projeto
gitignore_path="$target_project/.gitignore"
if [[ -f "$gitignore_path" ]]; then
  if ! grep -q "\.squad" "$gitignore_path"; then
    printf "\n# Antigravity Squad artifacts\n.squad/\n.agentes/\n" >> "$gitignore_path"
    echo "Adicionado .squad/ ao .gitignore de $target_project"
  fi
fi

echo "Squad instalado no workspace: $target_project/.agents"
echo "Reabra ou recarregue o Antigravity e invoque /antigravity-squad."
echo "MCP server: python3 '$target_project/.agents/mcp/server.py' (stdio)"
