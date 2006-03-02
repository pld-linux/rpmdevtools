%define emacs_sitestart_d  %{_datadir}/emacs/site-lisp/site-start.d
%define xemacs_sitestart_d %{_datadir}/xemacs/site-packages/lisp/site-start.d
%define spectool_version   1.0.7

Summary:	Fedora RPM Development Tools
Name:		fedora-rpmdevtools
Version:	1.5
Release:	0.1
License:	GPL
Group:		Development/Tools
URL:		http://fedoraproject.org/wiki/fedora-rpmdevtools
# rpminfo upstream: http://people.redhat.com/twoerner/rpminfo/bin/
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	8b9e391f9da90a78ccb62db05e961bc3
Source1:	http://people.redhat.com/nphilipp/spectool/spectool-%{spectool_version}.tar.bz2
# Source1-md5:	e2b1668f39c085807cae5a770c252dd5
# Required for tool operations
Requires:	cpio
Requires:	file
Requires:	perl-base
Requires:	python
Requires:	python-rpm
Requires:	sed
Requires:	wget
# Minimal RPM build requirements
Requires:	bzip2
Requires:	diffutils
Requires:	gcc
Requires:	gcc-c++
Requires:	gzip
Requires:	make
Requires:	patch
#Requires:	redhat-rpm-config
Requires:	rpm-build
Requires:	tar
Requires:	unzip
Provides:	%{name}-emacs = %{version}-%{release}
Provides:	spectool = %{spectool_version}
Obsoletes:	fedora-rpmdevtools-emacs < 0.1.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains scripts and (X)Emacs support files to aid in
development of Fedora RPM packages. These tools are designed for
Fedora Core 2 and later.

fedora-buildrpmtree     Create RPM build tree within user's home directory
fedora-installdevkeys   Install GPG keys in alternate RPM keyring
fedora-kmodhelper       Helper script for building kernel module RPMs
fedora-md5              Display the md5sum of all files in an RPM
fedora-newrpmspec       Creates new .spec from template
fedora-rmdevelrpms      Find (and optionally remove) "development" RPMs
fedora-rpmchecksig      Check package signatures using alternate RPM keyring
fedora-rpminfo          Prints information about executables and libraries
fedora-rpmvercmp        RPM version comparison checker
fedora-extract          Extract various archives, "tar xvf" style
fedora-diffarchive      Diff contents of two archives
fedora-wipebuildtree    Erase all files within dirs created by buildrpmtree
spectool                Expand and download sources and patches in specfiles

%prep
%setup -q -a 1
cp -p spectool*/README README.spectool

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-buildrpmtree    $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-installdevkeys  $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-kmodhelper      $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-md5             $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-newrpmspec      $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-rmdevelrpms     $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-rpmchecksig     $RPM_BUILD_ROOT%{_bindir}
install -pm 755 rpminfo                $RPM_BUILD_ROOT%{_bindir}/fedora-rpminfo
install -pm 755 fedora-extract         $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-diffarchive     $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-rpmvercmp       $RPM_BUILD_ROOT%{_bindir}
install -pm 755 fedora-wipebuildtree   $RPM_BUILD_ROOT%{_bindir}
install -pm 755 spectool*/spectool     $RPM_BUILD_ROOT%{_bindir}

install -dm 755 $RPM_BUILD_ROOT%{_prefix}/lib/rpm
install -pm 755 check-buildroot check-rpaths* \
  $RPM_BUILD_ROOT%{_prefix}/lib/rpm

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/fedora/devgpgkeys
install -pm 644 spectemplate*.spec template.init \
  $RPM_BUILD_ROOT%{_datadir}/fedora
install -pm 644 devgpgkeys/* $RPM_BUILD_ROOT%{_datadir}/fedora/devgpgkeys

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/fedora/emacs
install -pm 644 emacs/fedora-init.el $RPM_BUILD_ROOT%{_datadir}/fedora/emacs
for dir in %{emacs_sitestart_d} %{xemacs_sitestart_d} ; do
  install -dm 755 $RPM_BUILD_ROOT$dir
  ln -s %{_datadir}/fedora/emacs/fedora-init.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/fedora-init.elc
done

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/fedora
install -pm 644 rmdevelrpms.conf $RPM_BUILD_ROOT%{_sysconfdir}/fedora

%check
env PATH="$RPM_BUILD_ROOT%{_bindir}:$PATH" sh test/fedora-kmodhelper-test.sh
/bin/bash test/rpathtest.sh

%clean
rm -rf $RPM_BUILD_ROOT

# i don't use emacs, so dunno to check
%if 0
%triggerin -- emacs-common
[ -d %{emacs_sitestart_d} ] && \
  ln -sf %{_datadir}/fedora/emacs/fedora-init.el %{emacs_sitestart_d} || :

%triggerin -- xemacs-common
[ -d %{xemacs_sitestart_d} ] && \
  ln -sf %{_datadir}/fedora/emacs/fedora-init.el %{xemacs_sitestart_d} || :

%triggerun -- emacs-common
[ $2 -eq 0 ] && rm -f %{emacs_sitestart_d}/fedora-init.el* || :

%triggerun -- xemacs-common
[ $2 -eq 0 ] && rm -f %{xemacs_sitestart_d}/fedora-init.el* || :
%endif

%files
%defattr(644,root,root,755)
%doc README*
%config(noreplace) %{_sysconfdir}/fedora
%{_datadir}/fedora
%attr(755,root,root) %{_bindir}/fedora-*
%attr(755,root,root) %{_bindir}/spectool
%{_prefix}/lib/rpm/check-*
%ghost %{_datadir}/*emacs
