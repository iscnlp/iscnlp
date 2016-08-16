#!/bin/bash

GIT_LFS_VERSION="1.1.2"
GIT_LFS="git-lfs-${GIT_LFS_VERSION}/git-lfs"

echo "resetting travis remote"
git remote set-url origin "https://github.com/iscnlp/iscnlp.git"

echo "git lfs install"
GIT_TRACE=1 $GIT_LFS install

echo "fetch"
GIT_TRACE=1 $GIT_LFS fetch

echo "checkout"
GIT_TRACE=1 $GIT_LFS checkout
