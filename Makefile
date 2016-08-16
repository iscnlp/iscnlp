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
	git lfs install
	git lfs pull
