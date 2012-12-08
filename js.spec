%define _requires_exceptions devel(libnspr4\\|devel(libplc4\\|devel(libplds4

%define	major	1
%define	libname	%mklibname mozjs185_ %{major}
%define	devname	%mklibname mozjs185 -d

%define real_version 1.8.5

Summary:	SpiderMonkey, the Mozilla JavaScript engine
Name:		js
Version:	1.85
Release:	%mkrel 4
License:	MPL
Group:		Development/Other
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/%{name}185-1.0.0.tar.gz
Source100:	js.rpmlintrc
Patch0:		js-1.8.5-fix-destdir.patch

BuildRequires:	multiarch-utils >= 1.0.3
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
Requires:	%{libname} = %{EVRD}
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
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun 26 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:1.85-4mdv2011.0
+ Revision: 687247
- python as new BR
- backport fixes

* Wed May 04 2011 Funda Wang <fwang@mandriva.org> 1:1.85-2
+ Revision: 665888
- fix multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Apr 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.85-1
+ Revision: 649742
- add odd buildrequires on zip which autoconf script will crap out on if missing
- update to SpiderMonkey 1.8.5 and perform a whole lots of cleanups while at ti..

* Tue Jan 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.70-8
+ Revision: 632503
- use %%{EVRD}
- drop redundant dependency on library package
- enable parallel build
- enable unicode support
- compile with -fPIC

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-7mdv2011.0
+ Revision: 606113
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-6mdv2010.1
+ Revision: 519013
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:1.70-5mdv2010.0
+ Revision: 425472
- rebuild

* Sun Dec 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-4mdv2009.1
+ Revision: 316955
- fix build with -Werror=format-security (P7)
- use %%{ldflags} and fix linkage
- link against libedit and not editline

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-3mdv2009.0
+ Revision: 228617
- fix the exceptions to work on 64bit too

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-2mdv2009.0
+ Revision: 228590
- rule out some borked auto deps

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.70-1mdv2009.0
+ Revision: 228540
- 1.70
- sync with fedora

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1:1.5-6mdv2009.0
+ Revision: 221762
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 04 2008 Götz Waschk <waschk@mandriva.org> 1:1.5-5mdv2008.1
+ Revision: 161913
- fix devel provides and obsoletes

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1:1.5-4mdv2008.1
+ Revision: 150422
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Aug 29 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.5-3mdv2008.0
+ Revision: 73850
- bump release
- 1.5
- rediffed patches
- build it against system editline libs
- have to use -fno-stack-protector, otherwise it won't build


* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 18:04:13 (63395)
- bunzip patches

* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 17:59:17 (63394)
- Import js

* Fri Sep 01 2006 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 1.5-0.rc5a.10mdv2007.0
- add pkgconfig file

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.5-0.rc5a.9mdk
- rebuild

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.8mdk
- fix deps and conditional %%multiarch

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.7mdk
- revert latest "lib64 fixes"

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.6mdk
- lib64 fixes

* Mon Nov 22 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.5mdk
- relocate the headers as many dev moz packages seems to conflict
- nuke redundant provides

* Thu Sep 30 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.5-0.rc5a.4mdk
- fix fork off mozilla/js, our system knows about ISO C va_copy() macro

* Sun Jun 20 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.5-0.rc5a.3mdk
- fix ppc build

* Tue Jun 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.2mdk
- third try... (duh!)

* Tue Jun 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.1mdk
- second try...

* Tue Jun 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5a.1mdk
- 1.5-0.rc5a

* Mon Jun 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.5-0.rc5.6mdk
- rebuilt with gcc v3.4.x

