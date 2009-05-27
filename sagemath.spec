%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

%define		name			sagemath
%define		sagedir			%{_datadir}/sage
%define		sagedatadir		%{_localstatedir}/sage

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	3.4.2
Release:	%mkrel 1
Source0:	http://www.sagemath.org/src/sage-%{version}.tar
URL:		http://www.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	boost-devel
BuildRequires:	gcc-gfortran
BuildRequires:	libpari-devel
BuildRequires:	libatlas-devel
BuildRequires:	libblas-devel
BuildRequires:	libxml2-devel
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	flint-devel
BuildRequires:	fplll-devel
BuildRequires:	gd-devel
BuildRequires:	ghmm-devel
BuildRequires:	gsl-devel
BuildRequires:	iml
BuildRequires:	libm4ri-devel
BuildRequires:	mpfi-devel
BuildRequires:	ntl-devel
BuildRequires:	png-devel
BuildRequires:	polybori-devel
BuildRequires:	polybori-static-devel
BuildRequires:	pynac-devel
BuildRequires:	python-ghmm
BuildRequires:	python-processing
BuildRequires:	qd-static-devel
BuildRequires:	zn_poly-static-devel
BuildRequires:	linalg-linbox-devel
BuildRequires:	python-cython
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
BuildRequires:	flex bison
BuildRequires:	readline-devel
BuildRequires:	singular-devel
BuildRequires:	singular-static-devel
BuildRequires:	symmetrica-static-devel
BuildRequires:	scons

# This is actually, mainly a listing of spkgs
Requires:	bzip2
Requires:	clisp
Requires:	ecm
Requires:	flint

## flintqs-20070817.p3.spkg	( no longer available upstream )

Requires:	gap-system gap-system-packages
Requires:	gd-utils

## genus2reduction-0.3.p4.spkg 

Requires:	gcc-gfortran
Requires:	gp2c pari pari-data libpari-devel

## graphs-20070722.spkg 

Requires:	ipython
Requires:	jmol
Requires:	libatlas
Requires:	libblas

# FIXME unversioned .so
Requires:	libeclib-devel

Requires:	ntl
Requires:	libopencdk

# FIXME .a and .so files (this is also a sage specific library)
Requires:	libm4ri-devel

Requires:	lcalc
Requires:	linalg-linbox
Requires:	maxima

# Requires:	mercurial

Requires:	moin
Requires:	libmpfi-devel
Requires:	palp
Requires:	perl
Requires:	polymake

## polytopes_db-20080430.spkg

Requires:	pynac-devel
Requires:	python
Requires:	python-cvxopt
Requires:	python-cython
Requires:	python-gd
Requires:	python-ghmm
Requires:	python-gnutls
Requires:	python-jinja
Requires:	python-networkx
Requires:	python-matplotlib
Requires:	python-numpy
Requires:	python-pexpect
Requires:	python-polybori
Requires:	python-processing
Requires:	python-pycrypto
Requires:	python-pygments

# scipy should also provide the weave (http://www.scipy.org/Weave) dependency
Requires:	python-scipy
Requires:	python-sphinx
Requires:	python-sqlalchemy
Requires:	python-sqlite2
Requires:	python-sympy
Requires:	python-twisted-core
Requires:	python-twisted-web2
Requires:	R-base

## rubiks-20070912.p8.spkg

Requires:	singular
Requires:	symmetrica
Requires:	sympow
Requires:	tachyon

Obsoletes:	sagemath-doc < %{version}-%{release}

## FIXME some zope modules are required...
## Requires:	zope

Patch0:		sage-3.4.2.patch
Patch1:		sage-3.4.2-sage_scripts.patch
Patch2:		sage-3.4.2-env-vars.patch

# PyString_FromString() will crash if receiving a null string,
# that comes from dlerror if there are no errors, and the error
# was checking for libsingular.so at the wrong placd.
Patch3:		sage-3.4.2-libsingular.patch

Patch4:		sage-3.4.2-notebook.patch

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.


########################################################################
# %#package	doc
# Summary:	Documentation for sagemath
# Group:		Development/Other

# %#description	doc
# This package constains sagemath documentation.


########################################################################
%package	examples
Summary:	Sagemath example scripts and tests
Group:		Development/Other

%description	examples
This package constains sagemath example scripts and tests.


########################################################################
%prep
%setup -q -n sage-%{version}

mkdir -p spkg/build
tar jxf spkg/standard/sage-%{version}.spkg -C spkg/build
tar jxf spkg/standard/sage_scripts-%{version}.spkg -C spkg/build
rm -f spkg/build/sage_scripts-%{version}/*.orig
tar jxf spkg/standard/conway_polynomials-0.2.spkg -C spkg/build
tar jxf spkg/standard/elliptic_curves-0.1.spkg -C spkg/build
tar jxf spkg/standard/extcode-%{version}.spkg -C spkg/build
# tar jxf spkg/standard/doc-%#{version}.spkg -C spkg/build
tar jxf spkg/standard/examples-%{version}.spkg -C spkg/build
tar jxvf spkg/standard/dsage-1.0.spkg -C spkg/build

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


########################################################################
%build
export SAGE_ROOT=/
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`

export DESTDIR=%{buildroot}

pushd spkg/build/sage-%{version}
    pushd c_lib
	scons
    popd
    # some .c files are not (re)generated
    find . -name \*.pyx -o -name \*.pxd -exec touch {} \;
    python ./setup.py build
popd

pushd spkg/build/dsage-1.0/src
    python ./setup.py build
popd


########################################################################
%install
#rm -rf %#{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{sagedatadir}
mkdir -p %{buildroot}%{sagedir}/doc
# FIXME this is required for the notebook()
mkdir -p %{buildroot}%{sagedatadir}/extcode/sage

export DESTDIR=%{buildroot}

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
    mkdir -p %{buildroot}%{sagedir}/devel
    pushd sage
        find . -name \*.pxi -o -name \*.pxd -o -name \*.py -exec install -D -m 644 {} %{buildroot}%{sagedir}/devel/{} \;
	# install sage notebook templates
	mkdir -p %{buildroot}%{sagedatadir}/extcode/notebook/templates
	cp -fa server/notebook/templates/*.html %{buildroot}%{sagedatadir}/extcode/notebook/templates
    popd
    mkdir -p %{buildroot}%{sagedatadir}/extcode/notebook/html
    cp -fa doc/output/html/* %{buildroot}%{sagedatadir}/extcode/notebook/html
popd

pushd spkg/build/dsage-1.0/src
    python setup.py install --root=%{buildroot}
popd

#------------------------------------------------------------------------
pushd spkg/build/sage_scripts-%{version}
    mkdir -p %{buildroot}%{sagedir}/bin
    cp -fa sage-* dsage_* *doctest.py ipy_profile_sage.py %{buildroot}%{sagedir}/bin
    cp -far ipython %{buildroot}%{sagedir}
    cp -fa COPYING.txt %{buildroot}%{sagedir}
    pushd %{buildroot}%{sagedir}/bin
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/Singular sage_singular
	ln -sf %{_bindir}/gp sage_pari
    popd
popd

#------------------------------------------------------------------------
pushd spkg/build/conway_polynomials-0.2
    mkdir -p %{buildroot}%{sagedatadir}/conway_polynomials
    cp -fa src/conway_polynomials/* %{buildroot}%{sagedatadir}/conway_polynomials
popd

#------------------------------------------------------------------------
pushd spkg/build/elliptic_curves-0.1
    cp -fa cremona_mini/src/cremona_mini %{buildroot}%{sagedatadir}
    mkdir -p %{buildroot}%{sagedatadir}/ellcurves
    cp -fa ellcurves/rank* %{buildroot}%{sagedatadir}/ellcurves
popd

#------------------------------------------------------------------------
pushd spkg/build/extcode-%{version}
    mkdir -p %{buildroot}%{sagedatadir}/extcode
    cp -far gap images javascript maxima mwrank notebook pari pickle_jar sagebuild singular \
	%{buildroot}%{sagedatadir}/extcode
    pushd %{buildroot}%{sagedatadir}/extcode/notebook/java
	ln -sf %{_datadir}/jmol jmol
    popd
popd

#------------------------------------------------------------------------
# pushd spkg/build/doc-%{version}
#    cp -far html/* %{buildroot}/%{sagedir}/doc
# popd

#------------------------------------------------------------------------
rm -f %{buildroot}%{_bindir}/spkg-debian-maybe
pushd %{buildroot}%{sagedir}/bin/
    # not supported - only prebuilt packages for now
    rm -f sage-{bdist,build,build-debian,clone,crap,debsource,download_package,env,libdist,location,make_devel_packages,omega,pkg,pkg-nocompress,pull,push,sdist,sbuildhack,upgrade}
    rm -f sage-list-* sage-mirror* SbuildHack.pm sage-test-*
    rm -f sage-{verify-pyc,check-64}
    rm -f *~
    # osx only
    rm -f sage-{check-libraries.py,ldwrap,open,osx-open}
    # windows only
    rm -f sage-rebase_sage.sh
popd

#------------------------------------------------------------------------
mv -f %{buildroot}%{_prefix}/dsage/web %{buildroot}/%{sagedatadir}

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export CUR=\`pwd\`
export SAGE_ROOT="/"
export DOT_SAGE="\$HOME/.sage/"
mkdir -p \$DOT_SAGE
export SAGE_DOC="%{sagedir}/doc"
export SAGE_DATA="%{sagedatadir}"
export SAGE_LOCAL="%{sagedir}"
export PATH=%{sagedir}/bin:%{_datadir}/singular/%{_arch}:\$PATH
export SINGULARPATH=%{_datadir}/singular/LIB
%{sagedir}/bin/sage-sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{sagedir}/examples
pushd spkg/build/examples-%{version}
    cp -far ajax calculus comm_algebra example.py example.sage finance \
	fortran gsl latex_embed linalg misc modsym programming \
	test_all tests worksheets \
	%{buildroot}%{sagedir}/examples
popd


########################################################################
%clean
# rm -rf #%#{buildroot}


########################################################################
%files
%defattr(-,root,root)
%dir %{py_platsitedir}/sage
%{py_platsitedir}/*.egg-info
%{py_platsitedir}/sage/*
%dir %{sagedatadir}
%{sagedatadir}/*
%dir %{sagedir}
%{sagedir}/*
%{_bindir}/*
%{_libdir}/*.so


########################################################################
# %#files		doc
# %#dir %#{sagedir}/doc
# %#{sagedir}/doc/*


########################################################################
%files		examples
%dir %{sagedir}/examples
%{sagedir}/examples/*
