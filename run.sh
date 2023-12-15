ARXIV_ID=$1

if [ -z "$ARXIV_ID" ]; then
    echo "Usage: run.sh <arxiv_id>"
    exit 1
fi

# Ready the directory
rm -rf $ARXIV_ID
mkdir -p $ARXIV_ID

# Download the paper
paper $ARXIV_ID -p -d $ARXIV_ID
PDF_FN=$(ls -1 $ARXIV_ID/*.pdf | head -n 1)
echo $PDF_FN

# Extract the text
nougat $PDF_FN -o $ARXIV_ID
MMD_FN=$(echo $PDF_FN | sed 's/pdf/mmd/g')
echo $MMD_FN

# Translate English to Korean
python translate_mmd.py $MMD_FN

# Ready the templates
python ready_templates.py $MMD_FN

# Git add
git add $ARXIV_ID
git add README.md

# Git commit
git commit -m "Add $ARXIV_ID"

# Git push
git push
