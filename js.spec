%define _requires_exceptions devel(libnspr4\\|devel(libplc4\\|devel(libplds4

%define	major	1
%define	libname	%mklibname mozjs185_ %{major}
%define	devname	%mklibname mozjs185 -d

%define real_version 1.8.5

Summary:	SpiderMonkey, the Mozilla JavaScript engine
Name:		js
Version:	1.85
Release:	5
License:	MPL
Group:		Development/Other
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}185-1.0.0.tar.gz
Patch0:		js-1.8.5-fix-destdir.patch
BuildRequires:	nspr-devel
BuildRequires:	readline-devel
BuildRequires:	autoconf2.1
BuildRequires:	python
# wtf?
BuildRequires:	zip
Epoch:		1

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
The JavaScript engine compiles and executes scripts containing JavaScript
statements and functions. The engine handles memory allocation for the
objects needed to execute scripts, and it cleans up—garbage
collects—objects it no longer needs.

SpiderMonkey supports versions 1.0 through 1.8 of the JavaScript language.
JS 1.3 and later conform to the ECMAScript specification, ECMA 262-3.
Later versions also contain Mozilla extensions such as array comprehensions
and generators. SpiderMonkey also supports E4X (optionally).

%package -n	%{devname}
Summary:	The header files for %{libname}
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	libjs-devel = %{EVRD}
Provides:	mozjs-devel = %{EVRD}
Requires:	nspr-devel

%description -n	%{devname}
These are the header files for development with SpiderMonkey.

%prep
%setup -q -n %{name}-%{real_version}/js/src
%patch0 -p3 -b .destdir~
autoconf-2.13

%build
%configure2_5x	--enable-readline \
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

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

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
