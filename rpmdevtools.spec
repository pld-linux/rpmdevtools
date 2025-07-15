%define		spectool_version   1.0.10
Summary:	RPM Development Tools
Name:		rpmdevtools
Version:	7.10
Release:	0.1
Group:		Development/Tools
# rpmdev-setuptree is GPLv2, everything else GPLv2+
License:	GPL v2+ and GPL v2
URL:		https://fedorahosted.org/rpmdevtools/
Source0:	https://fedorahosted.org/released/rpmdevtools/%{name}-%{version}.tar.xz
# Source0-md5:	b2e7d7e8fbdbcae8c31b7249fd1dc615
Source1:	http://people.redhat.com/nphilipp/spectool/spectool-%{spectool_version}.tar.bz2
# Source1-md5:	d193612122f297ee4b37f1b04f605768
Patch0:		spectool-1.0.10-sourcenum.patch
Patch1:		spectool-1.0.10-problemtags-637000.patch
BuildRequires:	%{_bindir}/pod2man
BuildRequires:	help2man
BuildRequires:	python >= 2.4
BuildRequires:	python-rpm
Requires:	%{_bindir}/man
Requires:	diffutils
Requires:	fakeroot
Requires:	file
Requires:	findutils
Requires:	gawk
Requires:	grep
Requires:	python >= 2.4
Requires:	python-rpm
Requires:	rpm-build >= 4.4.2.3
Requires:	sed
Requires:	wget
Provides:	spectool = %{spectool_version}
Obsoletes:	fedora-rpmdevtools
BuildArch:	noarch
# For _get_cword in bash completion snippet
Conflicts:	bash-completion < 20080705
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains scripts to aid in development of RPM packages.

%prep
%setup -q -a 1
cp -p spectool-%{spectool_version}/README README.spectool
cd spectool-%{spectool_version}
%patch -P0 -p1
%patch -P1 -p1
cd ..

%build
%configure \
	--libdir=%{_prefix}/lib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# sane naming
mv $RPM_BUILD_ROOT/etc/bash_completion.d/%{name}{.bash-completion,}

install -p spectool-%{spectool_version}/spectool $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/devscripts.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/newspec.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/rmdevelrpms.conf

# templates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/spectemplate-*.spec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/template.init

%attr(755,root,root) %{_bindir}/annotate-output
%attr(755,root,root) %{_bindir}/checkbashisms
%attr(755,root,root) %{_bindir}/licensecheck
%attr(755,root,root) %{_bindir}/manpage-alert
%attr(755,root,root) %{_bindir}/rpmargs
%attr(755,root,root) %{_bindir}/rpmdev-*
%attr(755,root,root) %{_bindir}/rpmelfsym
%attr(755,root,root) %{_bindir}/rpmfile
%attr(755,root,root) %{_bindir}/rpminfo
%attr(755,root,root) %{_bindir}/rpmls
%attr(755,root,root) %{_bindir}/rpmpeek
%attr(755,root,root) %{_bindir}/rpmsodiff
%attr(755,root,root) %{_bindir}/rpmsoname
%attr(755,root,root) %{_bindir}/spectool
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%{_datadir}/%{name}

# bash-completion subpkg
/etc/bash_completion.d/%{name}
