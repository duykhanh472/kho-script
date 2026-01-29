#!/usr/bin/env bash
set -e

# Nhận thư mục repo từ argument
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <repo_directory>"
    exit 1
fi

REPO_DIR="$1"

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "'$REPO_DIR' không phải là git repository."
    exit 1
fi

cd "$REPO_DIR"

BRANCH="gh-pages"
RETURN_BRANCH="main"

UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u})
REMOTE=${UPSTREAM%%/*}

# Nếu đang ở branch khác main → nhớ lại
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Kiểm tra branch local
if git show-ref --quiet refs/heads/$BRANCH; then
    echo "Branch '$BRANCH' đã tồn tại (local)."
    git checkout $RETURN_BRANCH
    exit 0
fi

# Kiểm tra branch remote
if git ls-remote --exit-code --heads $REMOTE $BRANCH >/dev/null 2>&1; then
    echo "Branch '$BRANCH' tồn tại trên remote. Fetch về local..."
    git fetch $REMOTE $BRANCH:$BRANCH
    git checkout $RETURN_BRANCH
    exit 0
fi

# Nếu chưa tồn tại → tạo mới
echo "Branch '$BRANCH' chưa tồn tại. Đang tạo mới..."
git checkout --orphan $BRANCH
git rm -rf .
touch .gitkeep
git add .gitkeep
git commit -m "Initialize gh-pages branch"
git push $REMOTE $BRANCH

# Quay về main
git checkout $RETURN_BRANCH

echo "Đã tạo branch '$BRANCH' và quay về '$RETURN_BRANCH'."
