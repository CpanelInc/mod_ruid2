.PHONY: all

all: init
	git clean -dxf
	mock -v -r ea4-mod_ruid2-cent6-x86_64 --clean
	mock -v -r ea4-mod_ruid2-cent6-x86_64 --unpriv --resultdir SRPMS --buildsrpm --spec SPECS/ruid2.spec --sources SOURCES
	mock -v -r ea4-mod_ruid2-cent6-x86_64 --unpriv --resultdir RPMS SRPMS/mod_ruid2-0.9.8-2.el6.src.rpm

init: /var/cache/mock/ea4-mod_ruid2-epel-6-x86_64/root_cache/cache.tar.gz
	mock -v -r ea4-mod_ruid2-cent6-x86_64 --init --update
