#!/usr/bin/env bash
# Script de instalação do Antigravity Autonomous Engineering Squad para Linux / macOS / WSL

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/.antigravity"

echo -e "\n🚀 \033[1;36m[Antigravity Squad Installer]\033[0m\n"

if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "\033[1;31mErro: Pasta '.antigravity' não encontrada em $SCRIPT_DIR\033[0m"
    exit 1
fi

if [ "$1" == "--global" ] || [ "$1" == "-g" ]; then
    TARGET_DIR="$HOME/.gemini/antigravity-cli/skills/antigravity-squad"
    echo -e "📦 Instalando globalmente em: \033[1;33m$TARGET_DIR\033[0m"
    mkdir -p "$TARGET_DIR"
    cp -r "$SOURCE_DIR/"* "$TARGET_DIR/"
    echo -e "\033[1;32m✅ Esquadrão instalado globalmente com sucesso!\033[0m"
    exit 0
fi

TARGET_PROJECT="$1"
if [ -z "$TARGET_PROJECT" ]; then
    echo "Escolha como deseja instalar:"
    echo "1) No diretório atual ($(pwd))"
    echo "2) Digitar caminho de outro projeto"
    echo "3) Globalmente no Antigravity (~/.gemini/antigravity-cli)"
    echo "q) Cancelar"
    read -rp "Opção: " choice
    case "$choice" in
        1) TARGET_PROJECT="$(pwd)" ;;
        2) read -rp "Caminho do projeto: " TARGET_PROJECT ;;
        3) 
            TARGET_DIR="$HOME/.gemini/antigravity-cli/skills/antigravity-squad"
            mkdir -p "$TARGET_DIR"
            cp -r "$SOURCE_DIR/"* "$TARGET_DIR/"
            echo -e "\033[1;32m✅ Esquadrão instalado globalmente com sucesso!\033[0m"
            exit 0
            ;;
        *) echo "Cancelado."; exit 0 ;;
    esac
fi

DEST_DIR="$TARGET_PROJECT/.antigravity"
echo -e "\n📁 Copiando para: \033[1;33m$DEST_DIR\033[0m"
mkdir -p "$DEST_DIR"
cp -r "$SOURCE_DIR/"* "$DEST_DIR/"

echo -e "\033[1;32m✅ Instalação concluída com sucesso!\033[0m"
echo -e "Abra o Antigravity no projeto e execute no chat: \033[1;36m/teamwork [sua demanda aqui]\033[0m\n"
