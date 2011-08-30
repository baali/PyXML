Summary: XML libraries for python
Name: PyXML
Version: 0.8.4
Release: 19%{?dist}
Source: http://prdownloads.sourceforge.net/pyxml/PyXML-%{version}.tar.gz
Patch0: PyXML-0.7.1-intern.patch
Patch1: PyXML-0.8.4-cvs20041111-python2.4-backport.patch
Patch2: PyXML-memmove.patch
Patch3: PyXML-0.8.4-python2.6.patch

License: MIT and Python and ZPLv1.0 and BSD
Group: Development/Libraries
Requires: python
URL: http://pyxml.sourceforge.net/
BuildRequires: python python-devel expat-devel dos2unix
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

# Must have setuptools to build the package
# The build portions moved to a subpackage in F-8
%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

# Must have setuptools to build the package
# The build portions moved to a subpackage in F-8
%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

%description
An XML package for Python.  The distribution contains a
validating XML parser, an implementation of the SAX and DOM
programming interfaces and an interface to the Expat parser.

%prep
%setup -q

%patch0 -p1 -b .intern
%patch1 -p1 -b .python2.4-backport
%patch2 -p1
%patch3 -p1

# iconv to use utf8
for file in CREDITS ANNOUNCE doc/xml-howto.txt doc/xml-ref.txt README; do
  iconv -f iso8859-1 -t utf-8 -o tmp $file
  mv tmp $file
done

# use Unix style EOL
dos2unix doc/xmlproc/standard.css

%build
# build PyXML with system expat
# Make sure we don't use local one
rm -rf extensions/expat
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} -c 'import setuptools; execfile("setup.py")' build  --with-xslt --with-libexpat=%{_usr}

%install
rm -fr $RPM_BUILD_ROOT
python -c 'import setuptools; execfile("setup.py")' install --skip-build --root=$RPM_BUILD_ROOT --with-xslt

# set executable bits
for file in xslt/_4xslt.py dom/ext/c14n.py dom/html/GenerateHtml.py; do
  chmod +x $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_xmlplus/$file
done

# move messages files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/locale
for file in dom/de dom/en_US dom/fr; do
  mv $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_xmlplus/$file \
    $RPM_BUILD_ROOT/%{_datadir}/locale
done

%find_lang 4Suite %{name}

# better to use symlink to python's pyexpat library
# Resolves 614911
pushd $RPM_BUILD_ROOT/%{python_sitearch}/_xmlplus/parsers
rm -rf pyexpat.so
ln -s %{_libdir}/python2.6/lib-dynload/pyexpat.so pyexpat.so 
popd

%clean
rm -rf $RPM_BUILD_ROOT

%check
cd test
PYTHONPATH=.. python regrtest.py -v

%files -f %{name}
%defattr(-,root,root,-)
%doc LICENCE ANNOUNCE CREDITS README README.dom README.pyexpat README.sgmlop TODO doc/*
%{_bindir}/xmlproc_parse
%{_bindir}/xmlproc_val
%{python_sitearch}/*egg-info
%{python_sitearch}/_xmlplus

%changelog
* Tue Jul 20 2010 Roman Rakus <rrakus@redhat.com> - 0.8.4-19
- better to use symlink to python's pyexpat library
  Resolves: #614911
- Fixes acording to merge review (#226350)
- Added check routine

* Wed Jun 23 2010 Roman Rakus <rrakus@redhat.com> - 0.8.4-18
- Build with -fno-strict-aliasing CFLAG
  Resolves: #605105

* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.4-17.1
- Fix conditional for RHEL

* Mon Nov 02 2009 Roman Rakus <rrakus@redhat.com> - 0.8.4-17
- Use system expat library

* Fri Oct 30 2009 Roman Rakus <rrakus@redhat.com> - 0.8.4-16
- Fix buffer over read

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.8.4-14
- Another 'as' hiding in Stylesheet.py -> as_

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.8.4-12
- Patch for 'as' reserved keyword (bug #477783)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.4-11
- Rebuild for Python 2.6

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.4-10
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.4-9
- Autorebuild for GCC 4.3

* Fri Nov 02 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.4-8
- Modify package so that it produces Python Eggs.

* Tue Aug 21 2007 Florian La Roche <laroche@redhat.com> - 0.8.4-7
- rebuild

* Wed Apr 18 2007 Jeremy Katz <katzj@redhat.com> - 0.8.4-6
- rebuild so that things aren't statically linked with libpython

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.8.4-5
- rebuild against python 2.5

* Thu Jul 27 2006 Florian La Roche <laroche@redhat.com> - 0.8.4-4
- don't check memmove

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 0.8.4-3.2.2
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.4-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.4-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 0.8.4-3
- build with gcc-4

* Fri Feb 25 2005 Miloslav Trmac <mitr@redhat.com> - 0.8.4-2
- Rebuild, this should fix #149507

* Tue Nov 30 2004 Miloslav Trmac <mitr@redhat.com> - 0.8.4-1
- Update to PyXML-0.8.4

* Thu Nov 11 2004 Miloslav Trmac <mitr@redhat.com> - 0.8.4-0.cvs20041111.1
- Update to current CVS snapshot, Python 2.4b2 requires unreleased PyXML-0.8.4
- Backport xml.sax.saxutils fix from Python 2.4b2

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 0.8.3-7
- rebuild against python 2.4

* Wed Sep 29 2004 Miloslav Trmac <mitr@redhat.com> - 0.8.3-6
- Don't omit xml.xslt and xml.xpath (#133879)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Thomas Woerner <twoerner@redhat.com> 0.8.3-3
- removed lang tag: fixes #113268

* Mon Nov 17 2003 Tim Waugh <twaugh@redhat.com> 0.8.3-2
- Rebuild for Python 2.3.

* Sat Aug 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.8.3

* Wed Jun 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.8.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  6 2003 Mihai Ibanescu <misa@redhat.com> 0.7.1-9
- rebuilt against new python

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.7.1-7
- lib64'ize

* Thu Aug 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7.1-6
- Reenable expat. While most code works, some specify expat directly
  and fails. Fix #72698, but there is still broken code there (it just 
  goes on to other errors)

* Tue Aug 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7.1-5
- Disable expat support. Other parsers are included. Broken here, 
  broken in 0.8.0. This fixes #72698

* Fri Jun 28 2002 Trond Eivind Glomsrød <teg@redhat.com>
- A fix for the expatreader

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7.1-1
- 0.7.1

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7-4
- Rebuild

* Mon Jan 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7-3
- Remove xpath, xslt - use the ones in 4Suite
- patch the build script, it's broken

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7-1
- PyXML 0.7

* Wed Dec  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.6.6-2
- Add .pyo files
- Don't hardcode python version

* Tue Sep 18 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.6.6-1
- 0.6.6
- Build for python 2.2

* Tue Jul 24 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add python-devel to BuildRequires (#49820)

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Mark the locale-specific files as such

* Thu Jun  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Don't obsolete itself

* Mon May  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Initial build, it's no longer part of 4Suite


