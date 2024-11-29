#!/bin/bash
function version {
    git rev-parse HEAD | cut -c1-8
}

rm -rf  build
mkdir "build"
cp  deploy.sh build/
cp  Dockerfile build/
cp  -r jxhaiserver build/

echo $(version) > build/server.version
