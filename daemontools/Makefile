
# daemontools encore
NAME=daemontools-encore
VERSION=1.10

# # daemontools original
# NAME_DT=daemontools
# VERSION_DT=0.76
# 
# download-org:
# 	wget -c -P . http://cr.yp.to/daemontools/${NAME_DT}-${VERSION_DT}.tar.gz
# 	wget -c -P . http://smarden.org/pape/djb/manpages/${NAME_DT0-$7VERSION_DT}-man.tar.gz


slack:
	./daemontools.Slackbuild

rpm:
	rpmbuild -bb --define "_sourcedir `pwd`" --define "_version ${VERSION}" daemontools.spec

download:
	wget -c -P . http://untroubled.org/${NAME}/${NAME}-${VERSION}.tar.gz


