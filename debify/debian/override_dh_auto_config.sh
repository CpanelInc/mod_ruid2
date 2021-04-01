#!/bin/bash

source debian/vars.sh

: Building $name $version-$release $_arch $ns_name-mmn = $_httpd_mmn

$_httpd_apxs -l cap -c $module_name.c
mv .libs/$module_name.so .
strip -g $module_name.so
