#! /usr/bin/env sh
find . \
    -type f \
    -not -path "./subtrees/*" \
    -not -path "./.git/*" \
    -not -path "./media/*" \
    -not -path "./static/*" \
    -not -path "./site_static/*" \
    -not -path "./fixtures/*" \
    -not -path "*.pyc" \
    -not -path "*.json" \
    -not -path "*.sql" \
    -not -path "*.pdf" \
    -not -path "*.png" \
    -not -path "*.jpg" \
    -not -path "*.gif" \
    -not -path "*.mo" \
    -not -path "*.psd" \
    -not -path "*.ai" \
    -not -path "./*/.DS_Store" \
    -exec bash -c 'expand -t 4 "$0" > /tmp/e && mv /tmp/e "$0"' {} \;

