%global _hardened_build 1

Summary: TACACS+ daemon
Name: tac_plus
Version: F4.0.4.28
Release: 2%{?dist}
License: Cisco
Group: Networking/Servers
Source0: ftp://ftp.shrubbery.net/pub/tac_plus/tacacs-%{version}.tar.gz
Source1: tac_plus.conf
Source2: tac_plus.sysconfig
Source3: tac_plus.service
URL: http://www.shrubbery.net/tac_plus/

BuildRequires: gcc
BuildRequires: glibc
BuildRequires: make 
BuildRequires: flex 
BuildRequires: bison
BuildRequires: tcp_wrappers-devel
BuildRequires: pam-devel

Requires: glibc
Requires: tcp_wrappers
Requires: nss-softokn-freebl
Requires: pam

%systemd_requires

Provides: tacacs+
Provides: tac_pwd

%description
TACACS+ daemon

%package devel
Summary: TACACS+ development files.

%description devel
TACACS+ development files.

%prep
%autosetup -n tacacs-%{version}

%build
%configure --enable-acls \
           --enable-uenable \
           --with-pidfile=/var/run/tac_plus.pid \
           --with-acctfile=/var/log/tac_plus.acct \
           --with-logfile=/var/log/tac_plus.log
%{__make} %{?_smp_mflags}

%install
%makeinstall
install -D -m 600 %{SOURCE1} %{buildroot}%{_sysconfdir}/tac_plus.conf
install -D -m 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/tac_plus
install -D -m 600 %{SOURCE3} %{buildroot}%{_unitdir}/tac_plus.service

install -d %{buildroot}/var/log
touch %{buildroot}/var/log/tac_plus.{log,acct}

%post
%systemd_post tac_plus.service

%preun
%systemd_preun tac_plus.service

%postun
%systemd_postun_with_restart tac_plus.service

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING FAQ
%config(noreplace) %{_sysconfdir}/tac_plus.conf
%config(noreplace) %{_sysconfdir}/sysconfig/tac_plus
%{_unitdir}/tac_plus.service
%{_bindir}/tac_pwd
%{_libdir}/libtacacs.a
%{_libdir}/libtacacs.la
%{_libdir}/libtacacs.so*
%{_sbindir}/tac_plus
%{_mandir}/man5/tac_plus.conf.5.gz
%{_mandir}/man8/tac_plus.8.gz
%{_mandir}/man8/tac_pwd.8.gz
%{_datarootdir}/tacacs/do_auth.py
%{_datarootdir}/tacacs/do_auth.pyc
%{_datarootdir}/tacacs/do_auth.pyo
%{_datarootdir}/tacacs/tac_convert
%{_datarootdir}/tacacs/users_guide
/var/log/tac_plus.log
/var/log/tac_plus.acct

%files devel
%{_includedir}/tacacs.h

%changelog
* Tue Oct 20 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - F4.0.4.28-2
- Ensure log files are created
- Log to /dev/console when starting via systemd

* Tue Oct 20 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - F4.0.4.28-1
- Initial release for F4.0.4.28

