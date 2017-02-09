deploy:
	bash deploy.sh #create your own deploy/testing script
install:
	sudo snap install --force-dangerous zero*.snap
try:
	snapcraft prime
	snap try prime
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
publish: test
	snapcraft push zeronet*.snap
script:
	snapcraft clean scripts
	snapcraft prime
