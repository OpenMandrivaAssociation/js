%define	major	1
%define	libname	%mklibname mozjs185_ %{major}
%define	devname	%mklibname mozjs185 -d
%define staticname %mklibname mozjs185 -d -s

%define real_version 1.8.5

Summary:	SpiderMonkey, the Mozilla JavaScript engine
Name:		js
Epoch:		1
Version:	1.85
Release:	18
License:	MPL
Group:		Development/Other
Url:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}185-1.0.0.tar.gz
# by default JS ships with libffi 3.0.10
# it's very old version 
# that does not support an ARM64
Source1:	libffi-3.0.13.tar.gz
Source100:	js.rpmlintrc
Patch0:		js-1.8.5-fix-destdir.patch
Patch1:		spidermonkey-1.8.5-arm_respect_cflags-3.patch
Patch2:		js-64bitbigendian.patch
Patch3:		js185-libedit.patch
Patch4:		js-filter.patch

BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	nspr-devel
BuildRequires:	jemalloc-devel
BuildRequires:	pkgconfig(libedit)
BuildRequires:	readline-devel
BuildRequires:	autoconf2.1
BuildRequires:	python
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

autoconf-2.13
rm -rf ctypes/libffi/
tar -xf %{SOURCE1} -C ctypes
mv ctypes/libffi-3.0.13 ctypes/libffi/

%build
export CC=gcc
export CXX=g++
%configure2_5x \
	--disable-static \
	--enable-readline \
	--enable-jemalloc \
	--enable-threadsafe \
	--enable-ctypes \
	--with-system-nspr
%make

%install
%makeinstall_std

chmod 644 %{buildroot}%{_includedir}/js/*

# install binary
install -m755 shell/js -D %{buildroot}%{_bindir}/js
install -m755 jscpucfg -D %{buildroot}%{_bindir}/jscpucfg

%multiarch_includes %{buildroot}%{_includedir}/js/jsautocfg.h

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libmozjs185.so.%{major}*

%files -n %{devname}
%doc README.html
%dir %{_includedir}/js
%{multiarch_includedir}/js/jsautocfg.h
%{_includedir}/js/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/*.a
