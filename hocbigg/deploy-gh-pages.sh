#!/usr/bin/env bash
set -e

# Nhận thư mục repo từ argument
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <repo_directory>"
    exit 1
fi

REPO_DIR="$1"

FORCE_UPDATE=false

if [ "$2" = "--force-update" ]; then
    FORCE_UPDATE=true
fi

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "'$REPO_DIR' không phải là git repository."
    exit 1
fi

cd "$REPO_DIR"

TARGET_BRANCH="gh-pages"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u})
REMOTE=${UPSTREAM%%/*}

# Chỉ cho phép deploy khi main sạch
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "Bạn đang ở branch '$CURRENT_BRANCH'. Vui lòng checkout về 'main' trước khi deploy."
    exit 1
fi

if ! git diff-index --quiet HEAD --; then
    if [ "$FORCE_UPDATE" = false ]; then
        echo "Working tree chưa sạch. Vui lòng commit hoặc stash, hoặc dùng --force-update."
        exit 1
    else
        echo "⚠️  Working tree chưa sạch, nhưng tiếp tục do có --force-update."
    fi
fi

MAIN_COMMIT=$(git rev-parse HEAD)

git checkout -f $TARGET_BRANCH

# Kiểm tra lần build trước
if [ -f .last_build_commit ] && [ "$FORCE_UPDATE" = false ]; then
    LAST_COMMIT=$(cat .last_build_commit)
    if [ "$LAST_COMMIT" = "$MAIN_COMMIT" ]; then
        echo "Không có thay đổi mới trên main. Bỏ qua deploy."
        git checkout main
        exit 0
    fi
fi

git checkout main

# Đây là phần mình cần sửa để chạy cho nhiều dự án khác nhau
BUILD_DIR="out"
TMP_DIR="../out"

echo "Building the site..."

cd ..

python3 generate_hocbigg_curriculum.py "$REPO_DIR"
python3 generate_sitemap.py "$REPO_DIR"

cd "$REPO_DIR"

echo "Copy build output to temp dir..."
cp -r "$BUILD_DIR"/. "$TMP_DIR"/

# --------------------------------

echo "Switch to $TARGET_BRANCH..."
git checkout -f $TARGET_BRANCH

if [ "$(git rev-parse --abbrev-ref HEAD)" != "$TARGET_BRANCH" ]; then
    echo "Lỗi: không ở branch $TARGET_BRANCH"
    exit 1
fi

echo "Xoá nội dung cũ..."
git rm -rf .

echo "Copy nội dung mới..."
cp -r "$TMP_DIR"/. .

# Lưu commit main đã build
echo "$MAIN_COMMIT" > .last_build_commit

echo "Commit..."

git add .
git commit -m "Cập nhật trang: $(date '+%Y-%m-%d %H:%M:%S')"

echo "Push..."

git push $REMOTE $TARGET_BRANCH

echo "Quay lại branch ban đầu..."
git checkout $CURRENT_BRANCH

rm -rf "$TMP_DIR"

echo "Deploy hoàn tất."

