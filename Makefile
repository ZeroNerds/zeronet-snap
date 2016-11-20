test:
	sudo snap install --force-dangerous --devmode zero*.snap
cleanbuild:
	snapcraft cleanbuild
clean:
	rm -fv *.snap
	rm -fv *.tar.bz2
	snapcraft clean
build:
	snapcraft build
