#!/usr/bin/env bash
set -euo pipefail
cd src/app
go test .
docker build -t "sdvps-demo:${BUILD_NUMBER:-local}" .
