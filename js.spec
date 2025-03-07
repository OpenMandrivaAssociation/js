%define	major	1
%define	libname	%mklibname mozjs185_ %{major}
%define	devname	%mklibname mozjs185 -d
%define staticname %mklibname mozjs185 -d -s
%define _disable_lto 1

%define real_version 1.8.5

Summary:	SpiderMonkey, the Mozilla JavaScript engine
Name:		js
Epoch:		1
Version:	78.15.0
Release:	2
License:	MPL
Group:		Development/Other
Url:		https://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}185-1.0.0.tar.gz
# by default JS ships with libffi 3.0.10
# it's very old version
# that does not support an ARM64
Source1:	libffi-3.2.1.tar.gz
Source100:	js.rpmlintrc
Patch0:		js-1.8.5-fix-destdir.patch
Patch1:		spidermonkey-1.8.5-arm_respect_cflags-3.patch
Patch2:		js-64bitbigendian.patch
Patch3:		js185-libedit.patch
Patch4:		js-filter.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1178141 (http://hg.mozilla.org/mozilla-central/rev/a7b220e7425a)
Patch9:         js-1.8.5-array-recursion.patch
Patch10:        js-1.8.5-c++11.patch
Patch11:	aarch64.patch

BuildRequires:	nspr-devel
BuildRequires:	jemalloc-devel
BuildRequires:	pkgconfig(libedit)
BuildRequires:	readline-devel
BuildRequires:	autoconf2.1
BuildRequires:	python2
# wtf?
BuildRequires:	zip

%description
The JavaScript engine compiles and executes scripts containing JavaScript
statements and functions. The engine handles memory allocation for the
objects needed to execute scripts, and it cleans up—garbage
collects—objects it no longer needs.

SpiderMonkey supports versions 1.0 through 1.8 of the JavaScript language.
JS 1.3 and later conform to the ECMAScript specification, ECMA 262-3.
Later versions also contain Mozilla extensions such as array comprehensions
and generators. SpiderMonkey also supports E4X (optionally).

%package -n	%{libname}
Summary:	JavaScript engine library
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library for SpiderMonkey.

%package -n	%{devname}
Summary:	The header files for %{libname}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	mozjs-devel = %{EVRD}

%description -n	%{devname}
These are the header files for development with SpiderMonkey.

%package -n	%{staticname}
Summary:	Static library for %{libname}
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n	%{staticname}
Static library for %{libname}

%prep
%setup -qn %{name}-%{real_version}/js/src
%patch0 -p3 -b .destdir~
%patch1 -p3 -b .respectcflags~
%patch2 -p3 -b .bigendian
%patch3 -p3 -b .libed
%patch4 -p2 -b .jsf
%patch9 -p3 -b .array-recursion
%patch10 -p3 -b .c++11
%patch11 -p3 -b .arm64

# Rm parts with spurios licenses, binaries
# Some parts under BSD (but different suppliers): src/assembler
#rm -rf src/assembler src/yarr/yarr src/yarr/pcre src/yarr/wtf src/v8-dtoa
rm -rf ctypes/libffi t tests/src/jstests.jar tracevis v8

autoconf-2.13
rm -rf ctypes/libffi/
tar -xf %{SOURCE1} -C ctypes
mv ctypes/libffi-3.2.1 ctypes/libffi/

%build
export CC=gcc
export CXX=g++
%configure \
	--disable-static \
	--enable-readline \
	--enable-jemalloc \
	--enable-threadsafe \
	--with-system-nspr
%make

%install
%makeinstall_std

chmod 644 %{buildroot}%{_includedir}/js/*

# install binary
install -m755 shell/js -D %{buildroot}%{_bindir}/js
install -m755 jscpucfg -D %{buildroot}%{_bindir}/jscpucfg

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libmozjs185.so.%{major}*

%files -n %{devname}
%doc README.html
%dir %{_includedir}/js
%{_includedir}/js/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/*.a
