install:
	sudo snap install --force-dangerous zero*.snap
install-dev:
	sudo snap install --force-dangerous --devmode zero*.snap
cleanbuild:
	snapcraft cleanbuild
clean:
	rm -fv *.snap
	rm -fv *.tar.bz2
	snapcraft clean
build:
	snapcraft build
