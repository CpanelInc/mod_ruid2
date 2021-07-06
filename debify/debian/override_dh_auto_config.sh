#!/bin/bash

source debian/vars.sh

set -x

: Building $name $version-$release $_arch $ns_name-mmn = $_httpd_mmn

# pulled from apr-util
mkdir -p config
cp $ea_apr_config config/apr-1-config
cp $ea_apr_config config/apr-config
cp /usr/share/pkgconfig/ea-apr16-1.pc config/apr-1.pc
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config/apr-util-1.pc
cp /usr/share/pkgconfig/ea-apr16-1.pc config
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:`pwd`/config"
touch configure

$_httpd_apxs -l cap -c $module_name.c
mv .libs/$module_name.so .
strip -g $module_name.so
