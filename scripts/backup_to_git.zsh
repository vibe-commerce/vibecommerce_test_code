#!/bin/zsh
# Бэкап на GitHub
# Использование: ./scripts/backup_to_git.zsh "комментарий"
# Или через алиас: backup "комментарий"

COMMENT=${1:-"backup: $(date +%Y-%m-%d_%H-%M-%S)"}

echo "📦 Backing up..."
git add -A
git commit -m "$COMMENT"
git push origin main
echo "✅ Done: $COMMENT"
