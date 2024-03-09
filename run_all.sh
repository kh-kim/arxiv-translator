# Take multiple arguments
ARXIV_IDS=$@

# Loop through the arguments and call run.sh for each
for ARXIV_ID in $ARXIV_IDS; do
    echo "Processing $ARXIV_ID"
    bash run.sh $ARXIV_ID
done
