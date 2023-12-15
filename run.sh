ARXIV_ID=$1

if [ -z "$ARXIV_ID" ]; then
    echo "Usage: run.sh <arxiv_id>"
    exit 1
fi

# Ready the directory
rm -rf papers/$ARXIV_ID
mkdir -p papers/$ARXIV_ID

# Download the paper
paper $ARXIV_ID -p -d papers/$ARXIV_ID
PDF_FN=$(ls -1 papers/$ARXIV_ID/*.pdf | head -n 1)
echo $PDF_FN

# If the directory is empty, remove it
# Exit if the directory is empty
if [ ! "$(ls -A papers/$ARXIV_ID)" ]; then
    rm -rf papers/$ARXIV_ID
    exit 1
fi

# Extract the text
nougat $PDF_FN -o papers/$ARXIV_ID
MMD_FN=$(echo $PDF_FN | sed 's/pdf/mmd/g')
echo $MMD_FN

# Translate English to Korean
python translate_mmd.py $MMD_FN

# Ready the templates
python ready_templates.py $MMD_FN

# Git add
git add papers/$ARXIV_ID
git add README.md

# Git commit
git commit -m "Add $ARXIV_ID"

# Git push
git push
