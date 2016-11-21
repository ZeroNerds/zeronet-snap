all: #default task
	dir $(SNAPCRAFT_STAGE)
	mkdir $(SNAPCRAFT_STAGE)/usr/lib/python2.7/site-packages
	/usr/bin/pip install --install-option="--prefix=$(SNAPCRAFT_STAGE)/usr/lib/python2.7/site-packages" -r $(SNAPCRAFT_STAGE)/requirements.txt
install: #copy all the files
	#do something - maybe?
