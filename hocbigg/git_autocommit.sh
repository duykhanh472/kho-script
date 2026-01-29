#!/usr/bin/env bash
set -e

DIR="$1"

if [ -z "$DIR" ]; then
    echo "Usage: ./git_commit_this.sh <directory>"
    exit 1
fi

# Bỏ dấu / nếu có
DIR="${DIR%/}"

if [ ! -d "$DIR" ]; then
    echo "'$DIR' không tồn tại."
    exit 1
fi

# Kiểm tra có repo git không
if [ ! -d "$DIR/.git" ]; then
    echo "'$DIR' không phải git repository."
    exit 0
fi

cd "$DIR"

# Không có thay đổi → bỏ qua
if git diff-index --quiet HEAD --; then
    echo "[$DIR] Không có thay đổi."
    exit 0
fi

git add .
git commit -m "Update"

echo "[$DIR] Committed."