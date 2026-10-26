# Invoked by COPR make_srpm: make -f .copr/Makefile srpm outdir=<dir> spec=<path>
specdir := $(dir $(abspath $(spec)))

.PHONY: srpm
srpm:
	dnf -y install rpmdevtools rpm-build
	spectool -g -C $(specdir) $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(specdir)" \
		--define "_srcrpmdir $(outdir)"
