#!/bin/bash

OUTFILE=$(readlink -f package.zip)
VENV=$(pipenv --venv)
FUNCTION_NAME=andrews-bus-times-lambda

rm ${OUTFILE}

(cd ${VENV}/lib/python3.6/site-packages/ && zip -r9q ${OUTFILE} ./*)
zip -r9q ${OUTFILE} *.py

aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://${OUTFILE}
