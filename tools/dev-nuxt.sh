#!/usr/bin/env bash

set -o errexit

root="$(dirname "$0")/.."
app="${root}/frontend"

(
  cd "${app}"

  git config --global url."https://".insteadOf git://
  if [[ ! -d node_modules/.bin ]]; then
    echo "Installing dependencies"
    yarn install
  fi

  echo "Starting frontend server"
  yarn lintfix
  yarn dev
)
