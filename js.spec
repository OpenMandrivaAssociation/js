%define _requires_exceptions devel(libnspr4\\|devel(libplc4\\|devel(libplds4

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define epoch	1

%define real_version 1.7.0

Summary:	JavaScript engine
Name:		js
Version:	1.70
Release:	%mkrel 7
License:	MPL
Group:		Development/Other
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/js-%{real_version}.tar.gz
Patch1:		js-va_copy.diff
Patch2:		js-editline.diff
Patch3:		js-1.7.0-make.patch
Patch4:		js-shlib.patch
Patch5:		js-ldflags.patch
Patch6:		js-1.7.0-threadsafe.patch
Patch7:		js-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	edit-devel
BuildRequires:	nspr-devel
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Epoch:		%{epoch}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Obsoletes:	%{mklibname -d js 1}
Requires:	nspr-devel
Epoch:		%{epoch}

%description -n	%{develname}
These are the header files for %{libname}

%prep

%setup -q -n %{name}

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch1 -p1 -b .va_copy
%patch2 -p0 -b .editline
%patch3 -p1 -b .make
%patch4 -p0 -b .shlib
%patch5 -p0 -b .ldflags
%patch6 -p1 -b .threadsafe
%patch7 -p0 -b .format_not_a_string_literal_and_no_format_arguments

%build
export CFLAGS="%{optflags} -fno-stack-protector -DPIC -fPIC -D_REENTRANT"
export XCFLAGS="$CFLAGS"
export BUILD_OPT=1
export LDFLAGS="%{ldflags}"

make -C src -f Makefile.ref \
    JS_THREADSAFE="1" \
    XCFLAGS="$CFLAGS" \
    BUILD_OPT="1" \
    JS_EDITLINE="1" \
    LDFLAGS="%{ldflags}"

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
Libs: -L\${libdir} -ljs
Cflags: -I\${includedir}/js-%{version}
EOF

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/js-%{version}

# install headers
install -m0644 src/*.h %{buildroot}%{_includedir}/js-%{version}/
install -m0644 src/js.msg %{buildroot}%{_includedir}/js-%{version}/
install -m0644 src/*.tbl %{buildroot}%{_includedir}/js-%{version}/
install -m0644 src/Linux_All_OPT.OBJ/jsautocfg.h %{buildroot}%{_includedir}/js-%{version}/

# install shared library
install -m0755 src/Linux_All_OPT.OBJ/lib%{name}.so \
    %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

# install static library
install -m0644 src/Linux_All_OPT.OBJ/lib%{name}.a %{buildroot}%{_libdir}/

# install binary
install -m0755 src/Linux_All_OPT.OBJ/%{name} %{buildroot}%{_bindir}/
install -m0755 src/Linux_All_OPT.OBJ/jscpucfg %{buildroot}%{_bindir}/

# install pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 libjs.pc %{buildroot}%{_libdir}/pkgconfig/

%multiarch_includes %{buildroot}%{_includedir}/js-%{version}/jsautocfg.h

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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
%multiarch %{multiarch_includedir}/js-%{version}/jsautocfg.h
%{_includedir}/js-%{version}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
