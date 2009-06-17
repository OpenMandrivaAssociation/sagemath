%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

# Correct breakage of liblinbox.so and liblinboxsage.so
%define		_disable_ld_as_needed	1

%define		name			sagemath
%define		SAGE_ROOT		%{_datadir}/sage
%define		SAGE_LOCAL		%{SAGE_ROOT}/local
%define		SAGE_DEVEL		%{SAGE_ROOT}/devel
%define		SAGE_DOC		%{SAGE_ROOT}/doc
%define		SAGE_DATA		%{_localstatedir}/sage

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	4.0.1
Release:	%mkrel 1
Source0:	http://www.sagemath.org/src/sage-%{version}.tar
URL:		http://www.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	boost-devel
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	flex bison
BuildRequires:	flint-devel
BuildRequires:	fplll-devel
BuildRequires:	gap-system
BuildRequires:	gcc-gfortran
BuildRequires:	gd-devel
BuildRequires:	ghmm-devel
BuildRequires:	gsl-devel
BuildRequires:	iml
BuildRequires:	ipython
BuildRequires:	libatlas-devel
BuildRequires:	libblas-devel
BuildRequires:	libm4ri-devel
BuildRequires:	libpari-devel
BuildRequires:	libxml2-devel
BuildRequires:	linalg-linbox-devel
BuildRequires:	mpfi-devel
BuildRequires:	ntl-devel
BuildRequires:	png-devel
BuildRequires:	polybori-static-devel
BuildRequires:	pynac-devel
BuildRequires:	python-cython
BuildRequires:	python-ghmm
BuildRequires:	python-jinja
BuildRequires:	python-numpy-devel
BuildRequires:	python-processing
BuildRequires:	python-setuptools
BuildRequires:	python-sphinx
BuildRequires:	python-twisted-core
BuildRequires:	python-twisted-web2
BuildRequires:	qd-static-devel
BuildRequires:	readline-devel
BuildRequires:	scons
BuildRequires:	singular-devel
BuildRequires:	singular-static-devel
BuildRequires:	symmetrica-static-devel
BuildRequires:	zn_poly-static-devel

# This is actually, mainly a listing of spkgs
Requires:	bzip2
Requires:	clisp
Requires:	eclib-mwrank
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
Requires:	maxima xmaxima

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

## FIXME some zope modules are required...
## Requires:	zope

Patch0:		sage-4.0.1.patch

Patch1:		sage-4.0.1-sage_scripts.patch
Patch2:		sage-3.4.2-env-vars.patch

# PyString_FromString() will crash if receiving a null string,
# that comes from dlerror if there are no errors, and the error
# was checking for libsingular.so at the wrong placd.
Patch3:		sage-3.4.2-libsingular.patch

Patch4:		sage-4.0.1-notebook.patch

Patch5:		sage-3.4.2-doc.patch

#   Sage clisp uses a hack to disable readline support, that is set
# by another custom script. But either using clisp or sbcl backend,
# and --disable-readline maxima command line, etc, it always generates
# truncated output.
#   This patch just removes the requirement of an extra script that
# doesn't truly correct the problem.
#   The problem is somewhere else (sage uses python 2.5, earlier
# version of python-pexpect, etc... needs more debugging)
Patch6: 	sage-3.4.2-maxima.patch

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.


########################################################################
%package	doc
Summary:	Documentation for sagemath
Group:		Development/Other

%description	doc
This package constains sagemath documentation.


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
tar jxf spkg/standard/examples-%{version}.spkg -C spkg/build
tar jxf spkg/standard/dsage-1.0.1.spkg -C spkg/build
tar jxf spkg/standard/jsmath-3.6b.p1.spkg -C spkg/build
tar jxf spkg/standard/tinyMCE-3.2.0.2.p0.spkg -C spkg/build
tar jxf spkg/standard/jquery-1.2.6.p0.spkg -C spkg/build
tar jxf spkg/standard/jqueryui-1.6r807svn.p0.spkg -C spkg/build

%patch0 -p1
%patch1 -p1
#%#patch2 -p1
#%#patch3 -p1
%patch4 -p1
#%#patch5 -p1
#%#patch6 -p1

# if executing prep, clean buildroot
rm -rf %{buildroot}

export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
mkdir -p $SAGE_ROOT $SAGE_LOCAL $SAGE_DEVEL

# match sage rebuild setup
mkdir -p $SAGE_DEVEL/sage
ln -sf %{_builddir}/sage-%{version}/spkg/build/sage-%{version}/sage $SAGE_DEVEL/sage/sage

# match system packages as sage packages
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include

pushd spkg/build/sage-%{version}
    # some .c files are not (re)generated
    find . -name \*.pyx -o -name \*.pxd -exec touch {} \;
popd


########################################################################
%build
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}

# FIXME still required?
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`
export DESTDIR=%{buildroot}

pushd spkg/build/sage-%{version}
    pushd c_lib
	scons
    popd
    python ./setup.py build
popd

pushd spkg/build/dsage-1.0.1/src
    python ./setup.py build
popd


########################################################################
%install
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
export SAGE_DATA=%{buildroot}%{SAGE_DATA}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}

export DESTDIR=%{buildroot}

#rm -rf %#{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p $SAGE_DATA
mkdir -p $SAGE_DOC
# FIXME this is required for the notebook()
mkdir -p $SAGE_DATA/extcode/sage

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
    pushd sage
	# install sage notebook templates
	mkdir -p $SAGE_DATA/extcode/notebook/templates
	cp -fa server/notebook/templates/*.html $SAGE_DATA/extcode/notebook/templates
    popd
popd

pushd spkg/build/dsage-1.0.1/src
    python setup.py install --root=%{buildroot} --install-purelib=%{py_platsitedir}
popd

#------------------------------------------------------------------------
pushd spkg/build/sage_scripts-%{version}
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* dsage_* *doctest.py ipy_profile_sage.py $SAGE_LOCAL/bin
    cp -far ipython $SAGE_ROOT
    cp -fa COPYING.txt $SAGE_ROOT
    pushd $SAGE_LOCAL/bin
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/Singular sage_singular
	ln -sf %{_bindir}/gp sage_pari
	ln -sf %{_bindir}/gap gap_stamp
    popd
popd

#------------------------------------------------------------------------
rm -f %{buildroot}%{_bindir}/spkg-debian-maybe
pushd $SAGE_LOCAL/bin/
    # not supported - only prebuilt packages for now
    rm -f sage-{bdist,build,build-debian,clone,crap,debsource,download_package,env,libdist,location,make_devel_packages,omega,pkg,pkg-nocompress,pull,push,sdist,sbuildhack,upgrade}
    rm -f sage-list-* sage-mirror* SbuildHack.pm sage-test-*
    rm -f sage-{verify-pyc,check-64,spkg*}
    rm -f *~
    # osx only
    rm -f sage-{check-libraries.py,ldwrap,open,osx-open,README-osx.txt}
    # windows only
    rm -f sage-rebase_sage.sh
popd

#------------------------------------------------------------------------
pushd spkg/build/conway_polynomials-0.2
    mkdir -p $SAGE_DATA/conway_polynomials
    cp -fa src/conway_polynomials/* $SAGE_DATA/conway_polynomials
popd

#------------------------------------------------------------------------
pushd spkg/build/elliptic_curves-0.1
    cp -fa cremona_mini/src/cremona_mini $SAGE_DATA
    mkdir -p $SAGE_DATA/ellcurves
    cp -fa ellcurves/rank* $SAGE_DATA/ellcurves
popd

#------------------------------------------------------------------------
pushd spkg/build/extcode-%{version}
    mkdir -p $SAGE_DATA/extcode
    cp -far gap images maxima mwrank notebook pari pickle_jar sagebuild singular \
	$SAGE_DATA/extcode
    pushd $SAGE_DATA/extcode/notebook/java
	rm -f jmol && ln -sf %{_datadir}/jmol jmol
    popd
popd

#------------------------------------------------------------------------
rm -fr $SAGE_DATA/web &&
    mv -f %{buildroot}%{_prefix}/dsage/web $SAGE_DATA &&
    rmdir %{buildroot}%{_prefix}/dsage

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export CUR=\`pwd\`
export DOT_SAGE="\$HOME/.sage/"
mkdir -p \$DOT_SAGE
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_DATA="$SAGE_DATA"
export PATH=$SAGE_LOCAL/bin:%{_datadir}/singular/%{_arch}:\$PATH
export SINGULARPATH=%{_datadir}/singular/LIB
$SAGE_LOCAL/bin/sage-sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
pushd spkg/build/jsmath-3.6b.p1
    cp -far src/jsmath $SAGE_DATA/extcode/notebook/javascript
    rm -f $SAGE_DATA/extcode/javascript &&
	ln -sf %{SAGE_DATA}/extcode/notebook/javascript \
	    $SAGE_DATA/extcode
    mkdir -p $SAGE_DATA/extcode/notebook/javascript/jsmath/fonts
    cp -far src/msbm10 $SAGE_DATA/extcode/notebook/javascript/jsmath/fonts
popd

pushd spkg/build/tinyMCE-3.2.0.2.p0
    cp -far src/tinymce/jscripts/tiny_mce $SAGE_DATA/extcode/notebook/javascript
popd

pushd spkg/build/jquery-1.2.6.p0
    cp -f patches/jquery.event.extendedclick.js src/jquery-plugins
    cp -far src/jquery $SAGE_DATA/extcode/notebook/javascript
    mkdir -p $SAGE_DATA/extcode/notebook/javascript/jquery/plugins
    cp -far src/jquery-plugins/* $SAGE_DATA/extcode/notebook/javascript/jquery/plugins
popd

pushd spkg/build/jqueryui-1.6r807svn.p0
    cp -far patches/sage patches/flora src/themes
    mkdir -p $SAGE_DATA/extcode/notebook/javascript/jqueryui
    cp -far src/*LICENSE.txt src/themes src/ui/minified/* \
	$SAGE_DATA/extcode/notebook/javascript/jqueryui
popd

#------------------------------------------------------------------------
mkdir -p $SAGE_ROOT/examples
pushd spkg/build/examples-%{version}
    cp -far ajax calculus comm_algebra example.py example.sage finance \
	fortran gsl latex_embed linalg misc modsym programming \
	test_all tests worksheets \
	$SAGE_ROOT/examples
popd

#------------------------------------------------------------------------
# Build documentation, using %{buildroot} environment, as it needs
# to run and load sage python modules
pushd spkg/build/sage-%{version}/doc
    export DOT_SAGE=%{buildroot}/.sage
    export SAGE_DOC=`pwd`
    export PATH=%{buildroot}%{_bindir}:$SAGE_LOCAL/bin:%{_datadir}/singular/%{_arch}:$PATH
    export SINGULARPATH=%{_datadir}/singular/LIB
    export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_datadir}/singular/%{_arch}:$LD_LIBRARY_PATH
    export PYTHONPATH=%{buildroot}%{py_platsitedir}
    # there we go
    python common/builder.py all html
    cp -far output/html $SAGE_DOC
    rm -f $SAGE_DATA/extcode/notebook/html &&
	ln -sf %{SAGE_DOC}/html $SAGE_DATA/extcode/notebook/html
    # some "user setup" files will be installed there...
    rm -fr $DOT_SAGE
popd

# Script was used to build documentation 
perl -pi -e 's|%{buildroot}||g;' %{buildroot}%{_bindir}/sage

########################################################################
%clean
# rm -rf #%#{buildroot}


########################################################################
%files
%defattr(-,root,root)
%dir %{py_platsitedir}/sage
%{py_platsitedir}/*.egg-info
%{py_platsitedir}/sage/*
%dir %{SAGE_DATA}
%{SAGE_DATA}/*
%dir %{SAGE_ROOT}
%{SAGE_ROOT}/*
%{_bindir}/*
%{_libdir}/*.so


########################################################################
%files		doc
%dir %{SAGE_DOC}
%{SAGE_DOC}/*


########################################################################
%files		examples
%dir %{SAGE_ROOT}/examples
%{SAGE_ROOT}/examples/*
