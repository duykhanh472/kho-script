#!/usr/bin/env bash
set -e

EPUB="${FILES_DIR}/${BASE_NAME}.epub"
AZW3="${FILES_DIR}/${BASE_NAME}.azw3"
MOBI="${FILES_DIR}/${BASE_NAME}.mobi"
HTML="${FILES_DIR}/${BASE_NAME}.html"
TXT="${FILES_DIR}/${BASE_NAME}.txt"

# EPUB
pandoc "$DOC_PATH" -f markdown -t epub -s -o "$EPUB" \
  --metadata title="$TITLE" \
  --metadata author="$AUTHOR" \
  --metadata language="vi" \
  --css="$CSS_PATH"

# AZW3
ebook-convert "$EPUB" "$AZW3"

# MOBI
ebook-convert "$EPUB" "$MOBI"

# TXT
pandoc -f markdown -t plain "$DOC_PATH" > "$TXT"

# HTML
pandoc "$DOC_PATH" -s -o "$HTML"