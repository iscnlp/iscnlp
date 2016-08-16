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
	git clone git@github.com:github/git-lfs.git
	cd git-lfs
	git checkout 4457d7c7c5906025f753579f67f975792235b717
	script/bootstrap
	ls bin
	cd ..
	git-lfs/bin/git-lfs init
	git-lfs/bin/git-lfs fetch
