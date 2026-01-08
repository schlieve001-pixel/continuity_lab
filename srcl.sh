#!/bin/bash

# 1. Get the current branch name automatically
branch=$(git branch --show-current)

# 2. Add ALL changes (new files, edits, deletions)
git add .

# 3. Create a commit message
# If you type a message, use it. If not, use a timestamp.
if [ -z "$1" ]; then
  msg="Checkpoint: $(date '+%Y-%m-%d %H:%M:%S')"
else
  msg="$1"
fi

# 4. Commit and Push
git commit -m "$msg"
git push origin "$branch"

echo "------------------------------------------------"
echo "✅ Project state saved to GitHub (Branch: $branch)"
echo "------------------------------------------------"
