#!/bin/bash

echo "🍦 ハーゲンダッツハンズオン03 - Docker動作確認 🍦"
echo "================================================="

echo "📋 Dockerバージョン確認"
docker --version

echo ""
echo "🐳 Docker hello-world実行"
echo "================================================="
docker run hello-world

echo ""
echo "✅ Docker動作確認完了！"