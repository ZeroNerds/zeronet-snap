deploy:
	bash deploy.sh #create your own deploy/testing script
install:
	sudo snap install --force-dangerous zero*.snap
install-dev:
	sudo snap install --force-dangerous --devmode zero*.snap
dockerbuild:
	snapcraft-docker
cleanbuild:
	snapcraft cleanbuild
clean:
	rm -fv *.snap
	rm -fv *.tar.bz2
	snapcraft clean
build:
	snapcraft build
test: clean dockerbuild deploy
	@echo "Insert tests here"
