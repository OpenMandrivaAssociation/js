# if we don't deactivate debug packages there is one strange
# /usr/lib/debug/usr/lib64/U unpacked file on x86_64
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define epoch	1

Summary:	JavaScript engine
Name:		js
Version:	1.5
Release:	%mkrel 6
License:	MPL
Group:		Development/Other
URL:		http://www.gingerall.com/charlie/ga/xml/d_related.xml
Source0:	%{name}-%{version}.tar.gz
Patch0:		lib%{name}-%{version}.patch
Patch1:		js-va_copy.diff
Patch2:		js-editline.diff
Requires:	%{libname} = %{epoch}:%{version}-%{release}
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
Epoch:		%{epoch}
BuildRequires:	editline-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.

%package -n	%{libname}
Summary:	JavaScript engine library
Group:		System/Libraries
Epoch:		%{epoch}

%description -n	%{libname}
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.

%package -n	%{develname}
Summary:	The header files for %{libname}
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	libjs-devel = %{epoch}:%{version}-%{release}
Obsoletes: %mklibname -d js 1
Epoch:		%{epoch}

%description -n	%{develname}
These are the header files for %{libname}

%prep

%setup -q -n %{name}

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

cd src
%patch0 -p0 
cd ..
%patch1 -p1 -b .va_copy
%patch2 -p0 -b .editline

%build
cd src
perl -pi -e "s/-shared/-shared -lc -soname libjs.so.1/;" config/Linux_All.mk
#JMD: %make does *not* work!
export CFLAGS="%{optflags} -fno-stack-protector -DPIC -fPIC -D_REENTRANT"
export XCFLAGS="$CFLAGS"

BUILD_OPT=1 make -f Makefile.ref 

# create pkgconfig file
# pkgconfig can't find libjs without it
%{__cat} > libjs.pc << 'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libjs
Description: %{summary}
Version: %{version}
Libs: -L${libdir} -ljs
Cflags: -I${includedir}/js-%{version}
EOF

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/js-%{version}

# install headers
install -m0644 src/*.h %{buildroot}%{_includedir}/js-%{version}/
install -m0644 src/Linux_All_OPT.OBJ/jsautocfg.h %{buildroot}%{_includedir}/js-%{version}/

# install shared library
install -m0755 src/Linux_All_OPT.OBJ/lib%{name}.so \
    %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

# install static library
install -m0644 src/Linux_All_OPT.OBJ/lib%{name}.a %{buildroot}%{_libdir}/

# install binary
install -m0755 src/Linux_All_OPT.OBJ/%{name} %{buildroot}%{_bindir}/

# install pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 src/libjs.pc %{buildroot}%{_libdir}/pkgconfig/

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/js-%{version}/jsautocfg.h
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%doc src/README.html
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/js-%{version}
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/js-%{version}/jsautocfg.h
%endif
%{_includedir}/js-%{version}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
