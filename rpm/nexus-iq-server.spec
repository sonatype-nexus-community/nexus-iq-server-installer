Name:		nexus-iq-server
Version:	%%VERSION%%
Release:	%%RELEASE%%
Summary:	Nexus IQ Server
License:	Proprietary
Requires:       java-1.8.0-openjdk-headless
URL:		https://www.sonatype.com
Source0:	%%BUNDLE_FILE%%
Source1:        %{name}-%{version}-rpm.tar.gz
BuildRoot:	%{_tmppath}/nexus-iq-server
BuildArch:	noarch

#Prefix: /

%define __jar_repack %{nil}

%description
Nexus IQ Server

%prep
rm -rf ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}
mkdir -p ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}
cd ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}
tar -xz \
  -f %{SOURCE0}

tar -xz -f %{SOURCE1}

%build
cd ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/sonatype/iqserver
rsync -v -a ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}/ %{buildroot}/opt/sonatype/iqserver

mkdir -p %{buildroot}/opt/sonatype/sonatype-work/iqserver/log
#rsync -a ${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}/sonatype-work/iqserver/ %{buildroot}/opt/sonatype/sonatype-work/iqserver

#patch config
perl -p -i -e 's/sonatypeWork: \.\/sonatype-work\/clm-server/sonatypeWork: \/opt\/sonatype\/sonatype-work\/iqserver/g' %{buildroot}/opt/sonatype/iqserver/config.yml
perl -p -i -e 's/: \.\/log\//: \/opt\/sonatype\/sonatype-work\/iqserver\/log\//g' %{buildroot}/opt/sonatype/iqserver/config.yml
perl -p -i -e 's/VERSION=replaceMeIQServerVersion/VERSION=%%JAR_VERSION%%/g' %{buildroot}/opt/sonatype/iqserver/extra/daemon/nexus-iq-server

mkdir -p %{buildroot}/etc/init.d
ln -sf /opt/sonatype/iqserver/extra/daemon/nexus-iq-server %{buildroot}/etc/init.d/nexus-iq-server

%clean
rm -rf %{buildroot}

%pre
echo pre $1
if [ $1 = 1 ] || [ "$1" = "install" ]; then
[ -d /opt/sonatype/sonatype-work/iqserver ] || mkdir -p /opt/sonatype/sonatype-work/iqserver
# create user account
getent group iqserver >/dev/null || groupadd -r iqserver
getent passwd iqserver >/dev/null || \
	useradd -r -g iqserver -d /opt/sonatype/sonatype-work/iqserver -m -c "iqserver role account" -s /bin/bash iqserver
fi
# stop the service before upgrading
if [ $1 = 2 ]; then
  /sbin/service nexus-iq-server stop
elif [ "$1" = "upgrade" ]; then
  /usr/sbin/service nexus-iq-server stop
fi

%post
echo post $1
# start the service upon first installation
if [ $1 = 1 ]; then
  /sbin/chkconfig --add nexus-iq-server
  /sbin/service nexus-iq-server start
elif [ "$1" = "configure" ]; then
  update-rc.d nexus-iq-server defaults
  /usr/sbin/service nexus-iq-server start
fi
# start the service after upgrading
if [ $1 = 2 ]; then
  /sbin/service nexus-iq-server start
elif [ "$1" = "upgrade" ]; then
  /usr/sbin/service nexus-iq-server start
fi

%preun
echo preun $1
if [ $1 = 0 ]; then
  /sbin/service nexus-iq-server stop
  /sbin/chkconfig --del nexus-iq-server
elif [ "$1" = "remove" ]; then
  /usr/sbin/service nexus-iq-server stop
  update-rc.d nexus-iq-server remove
fi

%files
%defattr(-,root,root,-)
/etc/init.d/nexus-iq-server
/opt/sonatype/iqserver
%dir %config(noreplace) /opt/sonatype/iqserver/extra
%config(noreplace) /opt/sonatype/iqserver/config.yml
%config /opt/sonatype/iqserver/demo.bat
%config /opt/sonatype/iqserver/demo.sh
%config /opt/sonatype/iqserver/extra/daemon/nexus-iq-server
%defattr(-,iqserver,iqserver)
/opt/sonatype/sonatype-work/iqserver

%changelog
* Thu Jun 27 2019 Dan Rollo <drollo@sonatype.com>
initial .spec from prior work of Jason Swank, Rick Briganti, Alvin Gunkel
