GRAPH_DIR="graphs"

function generate_dot_file {
    NAME="$1"
    BASE_CMD="$2"
    DOT_FILE="${GRAPH_DIR}/${NAME}.dot"
    DOT_CMD="${BASE_CMD} > ${DOT_FILE}"
    echo ${DOT_CMD}
    echo $(eval $DOT_CMD)
}

function generate_pdf_file {
    NAME="$1"
    BASE_CMD="$2"
    PDF_FILE="${GRAPH_DIR}/${NAME}.pdf"
    PDF_CMD="${BASE_CMD} --output ${PDF_FILE}"
    echo ${PDF_CMD}
    echo $(eval $PDF_CMD)
}

function generate_files {
    NAME="$1"
    BASE_CMD="$2"
    generate_dot_file "${NAME}" "${BASE_CMD}"
    generate_pdf_file "${NAME}" "${BASE_CMD}"
}

echo "Creating simplified model graph for all apps..."
NAME="ccb_simplified"
BASE_CMD="./manage.py graph_models \
    --disable-fields \
    --all-applications"
generate_files "${NAME}" "${BASE_CMD}"
# open "${PDF_FILE}"

echo "Creating grouped model graph for all apps..."
NAME="ccb_grouped"
BASE_CMD="./manage.py graph_models \
    --group-models \
    --all-applications"
generate_files "${NAME}" "${BASE_CMD}"
# open "${PDF_FILE}"

echo "Creating full model graph for all apps..."
NAME="ccb_full"
BASE_CMD="./manage.py graph_models \
    --all-applications"
generate_files "${NAME}" "${BASE_CMD}"
# open "${PDF_FILE}"

while read NAME; do
    echo "Creating model graph for ${NAME} app..."
    BASE_CMD="./manage.py graph_models ${NAME}"
    generate_files "${NAME}" "${BASE_CMD}"
done < ${GRAPH_DIR}/ccb_models.txt
