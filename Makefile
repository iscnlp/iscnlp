travis:
	[ ! -d .testrepository ] || \
		find .testrepository -name "times.dbm*" -delete
	python setup.py build_ext -i
	python setup.py test --coverage \
		--coverage-package-name=iscnlp
	flake8 --max-complexity 10 iscnlp
clean:
	find . -iname "*.pyc" -exec rm -vf {} \;
	find . -iname "__pycache__" -delete
lfs:
	GIT_LFS_VERSION="1.1.2"
	GIT_LFS_LINK=https://github.com/github/git-lfs/releases/download/v${GIT_LFS_VERSION}/git-lfs-linux-amd64-${GIT_LFS_VERSION}.tar.gz
	GIT_LFS="git-lfs-${GIT_LFS_VERSION}/git-lfs"
	echo "downloading and untarring git-lfs binary" 
	wget $GIT_LFS_LINK
	tar -xvzf git-lfs-*${GIT_LFS_VERSION}.tar.gz
	echo "ls"
	ls
	echo "resetting travis remote"
	git remote set-url origin "https://github.com/iscnlp/iscnlp.git"
	echo "git lfs install"
	GIT_TRACE=1 $GIT_LFS install
	echo "fetch"
	GIT_TRACE=1 $GIT_LFS fetch
	echo "checkout"
	GIT_TRACE=1 $GIT_LFS checkout
