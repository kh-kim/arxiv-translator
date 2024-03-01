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

# Download HTML paper version from "https://arxiv.org/html/{arxiv_id}"
HTML_FN=papers/$ARXIV_ID/paper.raw.en.html
if [ ! -f $HTML_FN ]; then
    echo https://arxiv.org/html/$ARXIV_ID
    python download.py https://arxiv.org/html/$ARXIV_ID > $HTML_FN
fi

# If the directory is empty, remove it
# Exit if the directory is empty
if [ ! "$(ls -A papers/$ARXIV_ID)" ]; then
    rm -rf papers/$ARXIV_ID
    exit 1
fi

# Translate the paper with raw HTML
python translate_html.py --arxiv_id $ARXIV_ID

# Extract the text
CUDA_VISIBLE_DEVICES=0 nougat $PDF_FN -o papers/$ARXIV_ID
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
