#!/bin/bash

DIR=$(cd .; pwd)
TMP=${DIR}/tmp

REPO='registry.sensedeal.wiki:8443/ie/sdai-pdfs-ocr-torch-gpu:'
if [ $# -ne 1 ];then
    echo -e "Usage:\n \tbuild.sh version"
    exit 1
fi
VERSION="$1"

rm -rf $TMP && mkdir -p $TMP

cp -r conf/OCR_deploy $TMP/
cp -r conf/resnet50-19c8e357.pth $TMP/
cp -r conf/volume $TMP/
cp Dockerfile $TMP/

# Generate the rpc code
#python -m grpc_tools.protoc -I../rpc --python_out=$SERVER --grpc_python_out=$SERVER ../rpc/data.proto
#python -m grpc_tools.protoc -I../rpc --python_out=$SERVER --grpc_python_out=$SERVER ../rpc/pdf_ocr.proto

# Build docker image
cd $TMP

nvidia-docker build . -t "${REPO}${VERSION}"  --network host
#docker push "${REPO}${VERSION}"
#rm -rf $TMP
