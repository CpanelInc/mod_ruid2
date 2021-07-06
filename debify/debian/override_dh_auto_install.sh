#!/bin/bash

source debian/vars.sh

rm -rf $DEB_INSTALL_ROOT
mkdir -p $DEB_INSTALL_ROOT$_httpd_moddir
install -m755 $module_name.so $DEB_INSTALL_ROOT$_httpd_moddir/
# Install the config file
mkdir -p $DEB_INSTALL_ROOT$_httpd_modconfdir
install -m 644 ruid2.conf $DEB_INSTALL_ROOT$_httpd_modconfdir/
