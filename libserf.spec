%{?scl:%scl_package libserf}
%{!?scl:%global pkg_name %{name}}

%{?scl:
%filter_from_provides s|libserf*\.so.*||g;
%filter_setup
}

Name:           %{?scl_prefix}libserf
Version:        1.3.9
Release:        1%{?dist}
Summary:        High-Performance Asynchronous HTTP Client Library
License:        ASL 2.0
URL:            http://serf.apache.org/
Source0:        https://archive.apache.org/dist/serf/serf-%{version}.tar.bz2
BuildRequires:  apr-devel
BuildRequires:  apr-util-devel
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  %{?scl_prefix}scons
BuildRequires:  pkgconfig
Patch0:         %{pkg_name}-norpath.patch

%description
The serf library is a C-based HTTP client library built upon the Apache 
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       apr-devel%{?_isa}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n serf-%{version} -p1

# Shared library versioning support in scons is worse than awful...
# minimally, here fix the soname to match serf-1.2.x.  Minor version
# handling should be fixed too; really requires better upstream support:
# http://scons.tigris.org/issues/show_bug.cgi?id=2869
sed -i '/SHLIBVERSION/s/MAJOR/0/' SConstruct

%build

%if %{?scl:1}0
scl enable %{?scl} '
%endif
scons \
      CFLAGS="%{optflags}" \
      LIBDIR=%{_libdir} \
      PREFIX=%{_prefix} \
      %{?_smp_mflags}
%if %{?scl:1}0
'
%endif

%install
%if %{?scl:1}0
scl enable %{?scl} '
%endif
scons install --install-sandbox=%{buildroot}
%if %{?scl:1}0
'
%endif

find %{buildroot}%{_libdir} -type f -name '*.*a' -delete -print

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%if %{?scl:1}0
scl enable %{?scl} '
%endif
scons %{?_smp_mflags} check || true
%if %{?scl:1}0
'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE NOTICE
%{_libdir}/*.so.*

%files devel
%doc CHANGES README design-guide.txt
%{_includedir}/serf-1/
%{_libdir}/*.so
%{_libdir}/pkgconfig/serf*.pc

%changelog
* Wed Feb 15 2017 Jaroslaw Polok <jaroslaw.polok@cern.ch> - 1.3.9-1
- repackaged as Software Collection for CentOS 6/7

* Fri Sep 02 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.3.9-1
- Update to 1.3.9 (RHBZ #1372506)

* Sat Apr 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.3.8-3
- Add LDFLAGS provided by RPM

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 Joe Orton <jorton@redhat.com> - 1.3.8-1
- update to 1.3.8 (#1155115, #1155392)
- remove RPATHs (#1154690)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Christopher Meng <rpm@cicku.me> - 1.3.7-1
- Update to 1.3.7

* Tue Jun 17 2014 Christopher Meng <rpm@cicku.me> - 1.3.6-1
- Update to 1.3.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Christopher Meng <rpm@cicku.me> - 1.3.5-1
- Update to 1.3.5

* Mon Feb 17 2014 Joe Orton <jorton@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Wed Nov  6 2013 Joe Orton <jorton@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Require krb5-devel for libgssapi (#1027011)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-3
- SPEC cleanup.

* Thu Jun 13 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-2
- Fix the permission of the library.

* Sun Jun 09 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-1
- Initial Package.
