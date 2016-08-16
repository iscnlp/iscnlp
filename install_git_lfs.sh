#!/bin/bash

GIT_LFS_VERSION="1.1.2"
GIT_LFS_LINK=https://github.com/github/git-lfs/releases/download/v${GIT_LFS_VERSION}/git-lfs-linux-amd64-${GIT_LFS_VERSION}.tar.gz
GIT_LFS="git-lfs-${GIT_LFS_VERSION}/git-lfs"
echo "downloading and untarring git-lfs binary" 
wget -qO- $GIT_LFS_LINK | tar xvz
