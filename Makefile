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
	wget https://github.com/github/git-lfs/releases/download/v1.1.0/git-lfs-linux-amd64-1.1.0.tar.gz
	tar -zxvf git-lfs-linux-amd64-1.1.0.tar.gz
	export PATH=`pwd`/git-lfs-1.1.0:$PATH
	git config credential.helper store
	echo "https://emschorsch:$GITHUB_TOKEN@github.com" > ~/.git-credentials
	git lfs install
	git reset
	git lfs pull
