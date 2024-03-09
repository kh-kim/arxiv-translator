ARXIV_ID=$1

if [ -z "$ARXIV_ID" ]; then
    echo "Usage: remove.sh <arxiv_id>"
    exit 1
fi

# If the directory is found, remove it
if [ -d papers/$ARXIV_ID ]; then
    rm -rf papers/$ARXIV_ID
fi

# Update main README.md
python ready_templates.py

# Update Git
git rm -r papers/$ARXIV_ID
git add README.md
git commit -m "Remove $ARXIV_ID"
git push
