#!/usr/bin/env bash

set -e

DOCKERHUB_USERNAME="multiversenms"
TAG="latest"
BUILD_IMAGE=false
RUN_IMAGE=false
PUSH_IMAGE=false

usage() {
    echo "Usage: $0 [-b] (-r or -p)"
    exit 1
}

# Parse command-line options
while getopts ":brp" opt; do
    case $opt in
        b)
            BUILD_IMAGE=true
            ;;
        r)
            RUN_IMAGE=true
            ;;
        p)
            PUSH_IMAGE=true
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
        :)
            echo "Option -$OPTARG requires an argument."
            usage
            ;;
    esac
done


# Check if both -r and -p flags are used together
if [ "$RUN_IMAGE" = false ] && [ "$PUSH_IMAGE" = false ]; then
    echo "ERROR: Missing -r (run) or -p (push) flag."
    usage
fi

# Check if both -r and -p flags are used together
if [ "$RUN_IMAGE" = true ] && [ "$PUSH_IMAGE" = true ]; then
    echo "ERROR: -r (run) and -p (push) flags cannot be used together."
    usage
fi

# Log in to Docker Hub
if [ "$PUSH_IMAGE" = true ]; then
    docker login --username $DOCKERHUB_USERNAME
fi

# Build image
if [ "$BUILD_IMAGE" = true ]; then
    docker build --build-arg http_proxy=${http_proxy}\
        --build-arg https_proxy=${https_proxy} -t "multiverse-ipcollect" .
fi

# Push the tagged image to Docker Hub
if [ "$PUSH_IMAGE" = true ]; then
    docker tag multiverse-ipcollect multiversenms/ipcollect:latest
    docker push multiversenms/ipcollect:latest
fi

echo "http_proxy=$http_proxy"

# Run the local image
if [ "$RUN_IMAGE" = true ]; then
    docker run -i --rm --name "multiverse-ipcollect"\
        -p "8071:8071" -e "CONTROLLER=10.11.200.123"\
        -e "AMQP_BROKER=10.11.200.123" -e "NETCONF_PORT=830"\
        -e "NETCONF_USER=ocnos" -e "NETCONF_PASSWORD=ocnos"\
        -e "http_proxy=$http_proxy" -e "https_proxy=$https_proxy" "multiverse-ipcollect"
fi

# Log out from Docker Hub
if [ "$PUSH_IMAGE" = true ]; then
    docker logout
fi
