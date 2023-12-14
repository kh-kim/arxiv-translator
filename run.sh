ARXIV_ID=$1

if [ -z "$ARXIV_ID" ]; then
    echo "Usage: run.sh <arxiv_id>"
    exit 1
fi

rm -rf $ARXIV_ID
mkdir -p $ARXIV_ID

paper $ARXIV_ID -p -d $ARXIV_ID

PDF_FN=$(ls -1 $ARXIV_ID/*.pdf | head -n 1)
echo $PDF_FN

nougat $PDF_FN -o $ARXIV_ID
MMD_FN=$(echo $PDF_FN | sed 's/pdf/mmd/g')
echo $MMD_FN

python translate_mmd.py $MMD_FN

python ready_templates.py $MMD_FN
