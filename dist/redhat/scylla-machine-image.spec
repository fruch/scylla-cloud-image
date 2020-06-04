Name:           %{package_name}
Version:        %{version}
Release:        %{release}
Summary:        Scylla Machine Image
Group:          Applications/Databases

License:        ASL 2.0
URL:            http://www.scylladb.com/
Source0:        %{name}-%{version}-%{release}.tar
Requires:       scylla = %{version} scylla-python3 curl

BuildArch:      noarch

%global _python_bytecompile_errors_terminate_build 0
%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}

%description


%prep
%setup -q


%build

%install
rm -rf $RPM_BUILD_ROOT

install -d m755 $RPM_BUILD_ROOT%{_unitdir}
install -m644 %{cloud_provider}/scylla-image-setup.service $RPM_BUILD_ROOT%{_unitdir}/
install -d -m755 $RPM_BUILD_ROOT/opt/scylladb
install -d -m755 $RPM_BUILD_ROOT/opt/scylladb/scylla-machine-image
install -d -m755 $RPM_BUILD_ROOT/opt/scylladb/scylla-machine-image/lib
install -m644 lib/log.py $RPM_BUILD_ROOT/opt/scylladb/scylla-machine-image/lib
install -m755 %{cloud_provider}/scylla_configure.py %{cloud_provider}/scylla_create_devices \
$RPM_BUILD_ROOT/opt/scylladb/scylla-machine-image/
./tools/relocate_python_scripts.py \
    --installroot $RPM_BUILD_ROOT/opt/scylladb/scylla-machine-image/ \
    --with-python3 ${RPM_BUILD_ROOT}/opt/scylladb/python3/bin/python3 \
    %{cloud_provider}/scylla_image_setup %{cloud_provider}/scylla_login %{cloud_provider}/scylla_configure.py \
    %{cloud_provider}/scylla_create_devices
install -d -m755 $RPM_BUILD_ROOT/home
install -d -m755 $RPM_BUILD_ROOT/home/centos
install -m755 %{cloud_provider}/.bash_profile $RPM_BUILD_ROOT/home/centos

%pre
/usr/sbin/groupadd scylla 2> /dev/null || :
/usr/sbin/useradd -g scylla -s /sbin/nologin -r -d ${_sharedstatedir}/scylla scylla 2> /dev/null || :

%post
%systemd_post scylla-image-setup.service

%preun
%systemd_preun scylla-image-setup.service

%postun
%systemd_postun scylla-image-setup.service

%clean
rm -rf $RPM_BUILD_ROOT


%files
%license LICENSE
%defattr(-,root,root)

%config /home/centos/.bash_profile
%{_unitdir}/scylla-image-setup.service
/opt/scylladb/scylla-machine-image/*

%changelog
* Wed Nov 20 2019 Bentsi Magidovich <bentsi@scylladb.com>
- Rename package to scylla-machine-image
* Mon Aug 20 2018 Takuya ASADA <syuu@scylladb.com>
- inital version of scylla-ami.spec

