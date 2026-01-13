#!/bin/bash

# Simple sync script to push all changes to GitHub
# Usage: ./sync.sh "Your commit message"

if [ -z "$1" ]
then
    MSG="Update and maintenance: $(date +'%Y-%m-%d %H:%M:%S')"
else
    MSG="$1"
fi

echo "🚀 Syncing Stock News Pro to GitHub..."

# Add all files
git add .

# Commit with message
git commit -m "$MSG"

# Push to main branch
git push origin main

echo "✅ Done! Project is up to date on GitHub."
