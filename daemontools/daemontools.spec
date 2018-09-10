##
# DJB daemontools
##

%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}

%define debug_package %{nil}

%define _release   1
%define _version   1.10

%define vendor   packit
%define _prefix  /opt/daemontools
%define _docdir  %{_prefix}/doc
%define _mandir  %{_prefix}/man
%define _libdir  %{_prefix}/lib

%define name daemontools-encore
%define version %{_version}
%define release %{_release}.%{vendor}.%{disttype}%{distnum}

Summary: 	DJB daemontools - tools for managing UNIX services  
License: 	BSD like
Source0: 	http://untroubled.org/%{name}/%{name}-%{version}.tar.gz
Source1:	daemontools-functions
Source2:	etc_init_daemontools.conf
Source3:	systemd.daemontools.service
#Patch0: 	daemontools-0.76.errno.patch
URL:      http://untroubled.org/daemontools-encore
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		System Environment/Base
Vendor:   packit
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%description
daemontools-encore is a collection of tools for managing UNIX services.
It is derived from the public-domain release of daemontools by D. J.
Bernstein, which can be found at http://cr.yp.to/daemontools.html

daemontools-encore adds numerous enhancements above what daemontools
could do, while maintaining backwards compatibility with daemontools.
See the CHANGES file for more details on what features have been added.

Official source release can be found at:

    http://untroubled.org/daemontools-encore/

Development versions are available from github:

    https://github.com/bruceg/daemontools-encore

Original D. J. Bernstein release can be found at:

    http://cr.yp.to/daemontools.html

%prep 
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%setup -q 
# path
sed -i.orig -e 's|/command|%{_bindir}|' svscanboot.sh 

echo 'cc %{optflags}' > conf-cc
echo 'cc -s %{optflags}' > conf-ld
echo %{buildroot}/%{_prefix} > home
%{__make}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_bindir}  

for BFILE in $(cat BIN | cut -d : -f 6-6 | grep -v "^$")
do  
  %{__install} -m 755 $BFILE %{buildroot}%{_bindir}  
done  

for MFILE in $(cat MAN  | cut -d : -f 6-6 | grep -v "^$")
do
  gzip -9 $MFILE
  %{__install} -m 0644 $MFILE.gz %{buildroot}%{_mandir}/man8/
done

mkdir $RPM_BUILD_ROOT/service

%if %{disttype} == el && %{distnum} == 6
  mkdir -p %{buildroot}%{_sysconfdir}/init
  cp %{SOURCE2}  %{buildroot}%{_sysconfdir}/init/daemontools.conf
  sed -i -e 's|_PREFIX_|%{_bindir}|' %{buildroot}%{_sysconfdir}/init/daemontools.conf
%endif

%if %{disttype} == el && %{distnum} == 7
  mkdir -p %{buildroot}/usr/lib/systemd/system
  cp %{SOURCE3}  %{buildroot}/usr/lib/systemd/system/daemontools.service
  sed -i -e 's|_PREFIX_|%{_bindir}|' %{buildroot}/usr/lib/systemd/system/daemontools.service
%endif

# functions script
mkdir -p %{buildroot}%{_libdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_libdir}
# the path
sed -i -e 's|@DT_BIN_DIR@|%{_bindir}|' \
    %{buildroot}%{_libdir}/daemontools-functions

# profile.d sh
mkdir -p  %{buildroot}%{_sysconfdir}/profile.d
cat << \EOF > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
#
# djb daemontools paths
#
export PATH=%{_bindir}:$PATH
export MANPATH=%{_mandir}:${MANPATH}

EOF

#
# helpers
#
for CMD in  isdown isup remove start status stop restart
do
cat > %{buildroot}%{_bindir}/svc-$CMD << EOF
#!/bin/bash
#   
# djb daemontools helpers
# 
      
if [ ! -r  %{_libdir}/daemontools-functions ]; then
  echo "Daemontools functions not found."
  exit -6 #  NOT_CONFIGURED
fi  

. %{_libdir}/daemontools-functions

svc_$CMD \$1

EOF

chmod 755 %{buildroot}%{_bindir}/svc-$CMD

done

%post

%if %{disttype} == el && %{distnum} == 7
  systemctl enable daemontools
%endif

%if %{disttype} == el && %{distnum} == 6
if [ "$1" = "2" ]; then
  echo "(post) %{name} upgrading"
  /sbin/initctl stop daemontools
fi
  /sbin/initctl start daemontools
%endif

%preun

%if %{disttype} == el && %{distnum} == 7
if [ "$1" = "0" ]; then
  echo "(preun) %{name} uninstalling"
  systemctl disable daemontools
fi
%endif

%if %{disttype} == el && %{distnum} == 6
if [ "$1" = "0" ]; then
  echo "(preun) %{name} uninstalling"
  /sbin/initctl stop daemontools
fi
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root)
%doc CHANGES
%doc CHANGES.djb
%doc LICENSE
%doc README
%doc TODO

%dir /service

%{_bindir}/*
%{_mandir}/man8/*

%if %{disttype} == el && %{distnum} == 6
  %config %{_sysconfdir}/init/daemontools.conf
%endif

%if %{disttype} == el && %{distnum} == 7
  %config /usr/lib/systemd/system/daemontools.service
%endif

%{_libdir}/daemontools-functions
%{_sysconfdir}/profile.d/%{name}.sh


%changelog
* Wed Jan 20 2018 - daemontools-encore
- initial release

