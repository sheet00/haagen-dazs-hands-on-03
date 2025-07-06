#!/bin/bash

# uv環境セットアップスクリプト
# UV setup script

echo "🚀 uv環境のセットアップを開始します..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.." || exit 1

# 仮想環境が既に存在するかチェック
if [ -d ".venv" ]; then
    echo "⚠️  既存の仮想環境が見つかりました。"
    read -p "既存の環境を削除して再作成しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  既存の仮想環境を削除中..."
        rm -rf .venv
    else
        echo "ℹ️  既存の環境を使用します。"
    fi
fi

# 仮想環境を作成
if [ ! -d ".venv" ]; then
    echo "🏗️  仮想環境を作成中..."
    uv venv
    if [ $? -ne 0 ]; then
        echo "❌ 仮想環境の作成に失敗しました"
        exit 1
    fi
fi

# 依存関係をインストール
echo "📦 依存関係をインストール中..."
uv pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依存関係のインストールに失敗しました"
    exit 1
fi

echo "✅ uv環境のセットアップが完了しました！"
echo ""
echo "🎉 使用方法:"
echo "  方法1: source .venv/bin/activate でアクティベート"
echo "  方法2: uv run python script.py で実行"
echo ""