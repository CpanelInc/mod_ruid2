# Namespace
%global ns_name ea-apache24
%global module_name mod_ruid2

Summary: Run all httpd process under user's access right.
Name: %{ns_name}-%{module_name}
Version: 0.9.8
Vendor: cPanel, Inc.
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4558 for more details
%define release_prefix 14
Release: %{release_prefix}%{?dist}.cpanel
Group: System Environment/Daemons
URL: http://sourceforge.net/projects/mod-ruid/
Source0: http://sourceforge.net/projects/mod-ruid/files/mod_ruid2/mod_ruid2-%{version}.tar.bz2
License: Apache Software License version 2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{ns_name}-devel >= 2.4.0 libcap-devel
BuildRequires: libtool
# NOTE: These 2 BuildRequires statements are needed because of a decision
# we made in EA4 to allow the user to pick and choose which mpm to work
# with.  Unfortunately, this prevents YUM from solving dependencies
# because it doesn't know which package to use.  This tells YUM which
# to use so it can build this MPM.  We may need to revert this opinion
# in the future.
BuildRequires: %{ns_name}-mpm = forked
BuildRequires: %{ns_name}-mod_cgi
Requires: %{ns_name}-mpm = forked
Requires: %{ns_name}-mmn = %{_httpd_mmn}
Requires: %{ns_name} >= 2.4.0 libcap
Obsoletes: mod_ruid mod_ruid2
Conflicts: %{ns_name}-mod_suexec %{ns_name}-mod_suphp %{ns_name}-mpm_itk
Conflicts: %{ns_name}-mod_fcgid
Conflicts: %{ns_name}-mod_cache
Provides: %{ns_name}-exec_code_asuser

Patch0: 0001-mailman-compatibility.patch
Patch1: 0002-added-rgroupinherit-flag.patch

%description
With this module, all httpd process run under user's access right, not nobody or apache.
mod_ruid2 is similar to mod_suid2, but has better performance than mod_suid2 because it
doesn't need to kill httpd children after one request. It makes use of kernel capabilites
and after receiving a new request suids again. If you want to run apache modules, i.e.
WebDAV, PHP, and so on under user's right, this module is useful.

%prep
: Building %{name} %{version}-%{release} %{_arch} %{ns_name}-mmn = %{_httpd_mmn}
%setup -q -n %{module_name}-%{version}
%patch0 -p1 -b .mailman
%patch1 -p1 -b .rgroupinherit

%build
%{_httpd_apxs} -l cap -c %{module_name}.c
mv .libs/%{module_name}.so .
%{__strip} -g %{module_name}.so

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_httpd_moddir}
install -m755 %{module_name}.so %{buildroot}%{_httpd_moddir}/

# Install the config file
mkdir -p %{buildroot}%{_httpd_modconfdir}
install -m 644 ruid2.conf %{buildroot}%{_httpd_modconfdir}/
    
%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root)%{_httpd_moddir}/*.so
%config(noreplace) %{_httpd_modconfdir}/*.conf


%changelog
* Tue May 16 2017 Dan Muey <dan@cpanel.net< - 0.9.8-14
- EA-5973: Conflict w/ Apache mod_cache like ea3 did

* Mon Oct 17 2016 Edwin Buck <e.buck@cpanel.net> - 0.9.8-13
- EA-5429: Added conflicts with mod_fcgid.

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 0.9.8-12
- EA-4383: Update Release value to OBS-proof versioning

* Tue Aug 04 2015 Dan Muey <dan@cpanel.net> 0.9.8-7
Add forked MPM to requires list

* Wed Jun 02 2015 Darren Mobley <darren@cpanel.net> 0.9.8-6
- Fixed typo in dependency

* Thu May 28 2015 Julian Brown <julian.brown@cpanel.net> 0.9.8-5
- Corrected ns_name from ea_apache24 to ea-apache24

* Thu May 28 2015 Julian Brown <julian.brown@cpanel.net> 0.9.8-4
- Now uses ea-apache24 RPM provided by EA4

* Mon Mar 16 2015 S. Kurt Newman <kurt.newman@cpanel.net> 0.9.8-3
- Now uses ea-apache24 RPM provided by EA4

* Thu Jan 08 2014 S. Kurt Newman <kurt.newman@cpanel.net> 0.9.8-2
- Updated for Apache 2.4 directory locations

* Fri Mar 22 2013 Kees Monshouwer <km|monshouwer_com> 0.9.8-1
- Address reported security bug in chroot mode. Thanks to the
  "cPanel Security Team" for the discovery of this bug.
- Improve chroot behavior in drop capability mode.

* Wed Apr 11 2012 Kees Monshouwer <km|monshouwer_com> 0.9.7-1
- Update to 0.9.7
- Reduction of memory usage, especially in large deployments

* Wed Apr 11 2012 Kees Monshouwer <km|monshouwer_com> 0.9.6-1
- Update to 0.9.6
- Fixed: user group exchange in default config

* Wed Mar 07 2012 Kees Monshouwer <km|monshouwer_com> 0.9.5-1
- Update to 0.9.5
- Switch default mode to 'config' !!!
- Apache 2.4 compatibility

* Wed Feb 23 2011 Kees Monshouwer <km|monshouwer.com> 0.9.4-1
- Update to 0.9.4
- Fixed: mod_security incompatibility issue

* Tue Jan 04 2011 Kees Monshouwer <km|monshouwer_com> 0.9.3-1
- Update to 0.9.3
- Fixed: chroot issue with sub-requests caused by mod_rewrite 

* Tue Dec 20 2010 Kees Monshouwer <km|monshouwer_com> 0.9.2-1
- Update to 0.9.2
- Fixed: array subscript was above array bounds in ruid_set_perm

* Mon Oct 18 2010 Kees Monshouwer <km|monshouwer_com> 0.9.1-1
- Update to 0.9.1

* Wed Jun 23 2010 Kees Monshouwer <km|monshouwer_com> 0.9-1
- Added chroot functionality 
- Update to 0.9

* Mon Jun 21 2010 Kees Monshouwer <km|monshouwer_com> 0.8.2-1
- Added drop capability mode to drop capabilities permanent after set[ug]id
- Update to 0.8.2

* Thu May 27 2010 Kees Monshouwer <km|monshouwer_com> 0.8.1-1
- Changed module name to mod_ruid2
- Update to 0.8.1

* Mon Apr 12 2010 Kees Monshouwer <km|monshouwer_com> 0.8-1
- Update to 0.8

* Wed Oct 21 2009 Kees Monshouwer <km|monshouwer_com> 0.7.1-1
- Fixed security problem in config

* Sun Sep 27 2009 Kees Monshouwer <km|monshouwer_com> 0.7-1
- Added per directory config option

* Wed Aug 29 2007 Kees Monshouwer <km|monshouwer_com> 0.6-3.1
- Build for CentOS 5

* Fri Sep 07 2006 Kees Monshouwer <km|monshouwer_com> 0.6-3
- Fixed first child request groups bug

* Fri Sep 07 2006 Kees Monshouwer <km|monshouwer_com> 0.6-2
- Fixed some uninitalized vars and a typo
- Changed the default user and group to apache 

* Wed Mar 08 2006 Kees Monshouwer <km|monshouwer_com> 0.6-1
- Inital build for CentOS 4.2
