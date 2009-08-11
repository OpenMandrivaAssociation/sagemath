%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

# Correct breakage of liblinbox.so and liblinboxsage.so
%define		_disable_ld_as_needed	1

%define		name			sagemath
%define		SAGE_ROOT		%{_datadir}/sage
%define		SAGE_LOCAL		%{SAGE_ROOT}/local
%define		SAGE_DEVEL		%{SAGE_ROOT}/devel
%define		SAGE_DOC		%{SAGE_ROOT}/doc
%define		SAGE_DATA		%{SAGE_ROOT}/data

# Need this because as of sage 4.0.1, it only works "correctly" with python-pexpect 2.0
%define		use_sage_pexpect	1
%define		SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	4.1
Release:	%mkrel 8
Source0:	http://www.sagemath.org/src/sage-%{version}.tar
Source1:	moin-1.5.7-filesystem.tar.bz2
URL:		http://www.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#------------------------------------------------------------------------
BuildRequires:	texlive-latex
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
BuildRequires:	ratpoints
BuildRequires:	readline-devel
BuildRequires:	scons
BuildRequires:	singular-devel
BuildRequires:	singular-static-devel
BuildRequires:	symmetrica-static-devel
BuildRequires:	zn_poly-static-devel

#------------------------------------------------------------------------
Requires:	bzip2
Requires:	clisp
Requires:	eclib-mwrank
Requires:	ecm
Requires:	flint
Requires:	fplll

## flintqs-20070817.p3.spkg	( no longer available upstream )

Requires:	gap-system gap-system-packages
Requires:	gd-utils

## genus2reduction-0.3.p4.spkg 

Requires:	gcc-gfortran
Requires:	gfan
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

# FIXME only enough dependencies to run example.sage were added to distro
# see package url for information on other listed dependencies
Requires:	python-zodb3

Requires:	R-base

## rubiks-20070912.p8.spkg

Requires:	singular
Requires:	symmetrica
Requires:	sympow
Requires:	tachyon

#------------------------------------------------------------------------
Obsoletes:	sage-doc <= 3.4.2
Obsoletes:	sage-examples <= 3.4.2

#------------------------------------------------------------------------
Patch0:		sage-4.1.patch
Patch1:		sage-4.1-sage_scripts.patch
Patch2:		sage-4.1-notebook.patch
Patch3:		sage-4.1-wiki.patch
Patch4:		sage-4.1-doc.patch
Patch5:		sage-4.1-dsage.patch

#------------------------------------------------------------------------
%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.


########################################################################
%prep
%setup -q -n sage-%{version}

pushd spkg
    mkdir -p build
    for pkg in	conway_polynomials-0.2		\
		dsage-1.0.1.p0			\
		elliptic_curves-0.1		\
		examples-%{version}		\
		extcode-%{version}		\
		genus2reduction-0.3.p5		\
		graphs-20070722			\
		jquery-1.2.6.p0			\
		jqueryui-1.6r807svn.p0		\
		jsmath-3.6b.p1			\
		polytopes_db-20080430		\
		sage-%{version}			\
		sage_scripts-%{version}		\
		tinyMCE-3.2.0.2.p0		\
    ; do
	tar jxf standard/$pkg.spkg -C build
    done
    rm -f build/sage_scripts-%{version}/*.orig

%if %{use_sage_pexpect}
    tar jxf standard/pexpect-2.0.p4.spkg -C build
%endif
popd

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

#------------------------------------------------------------------------
pushd spkg/build/genus2reduction-0.3.p5/src
# based on debian patch
cat > Makefile << EOF
CFLAGS = -O2 -I%{_includedir}/pari
LDFLAGS = -lpari
CC = gcc

genus2reduction:
	\${CC} \${CFLAGS} \${LDFLAGS} -o genus2reduction genus2reduction.c

install: genus2reduction
	mkdir -p \${DESTDIR}/%{SAGE_LOCAL}/bin
	install -p \$< \${DESTDIR}/%{SAGE_LOCAL}/bin

clean:
	rm -f genus2reduction
EOF
popd


########################################################################
%build
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}

export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`

export DESTDIR=%{buildroot}

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    pushd c_lib
	scons
    popd
    # some .c files are not (re)generated
    find . \( -name \*.pyx -o -name \*.pxd \) -exec touch {} \;
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/dsage-1.0.1.p0/src
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/genus2reduction-0.3.p5/src
    %make
popd


########################################################################
%install
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
export SAGE_DATA=%{buildroot}%{SAGE_DATA}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}

export DESTDIR=%{buildroot}

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
rm -fr $SAGE_DEVEL/sage $SAGE_LOCAL/{include,lib,share}
mkdir -p $SAGE_DATA $SAGE_DOC $SAGE_DEVEL/sage $SAGE_LOCAL/notebook/javascript
ln -sf %{_builddir}/sage-%{version}/spkg/build/sage-%{version}/sage $SAGE_DEVEL/sage/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
# install moin changes
pushd %{buildroot}
    tar jxf %{SOURCE1}
%ifarch x86_64 ppc64
    # move files in /usr/lib/python... to /usr/lib64/python...
    mkdir -p ./%{py_platsitedir}/MoinMoin
    mv ./%{py_puresitedir}/MoinMoin/* ./%{py_platsitedir}/MoinMoin
    rm -fr ./%{py_puresitedir}/MoinMoin
%endif
popd

# make jsMath available to moin
mkdir -p %{buildroot}%{_datadir}/moin/htdocs
ln -sf %{_datadir}/sage/local/notebook/javascript/jsmath %{buildroot}%{_datadir}/moin/htdocs/jsmath

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
    pushd sage
	# install sage notebook templates
	cp -fa server/notebook/templates %{buildroot}%{py_platsitedir}/sage/server/notebook
    popd
popd

pushd spkg/build/dsage-1.0.1.p0/src
    python setup.py install --root=%{buildroot} --install-purelib=%{py_platsitedir}
popd

#------------------------------------------------------------------------
%if %{use_sage_pexpect}
pushd spkg/build/pexpect-2.0.p4/src
    mkdir -p %{buildroot}%{SAGE_PYTHONPATH}
    cp -f {ANSI,FSM,pexpect,pxssh,screen}.py %{buildroot}%{SAGE_PYTHONPATH}
popd
%endif

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
pushd spkg/build/genus2reduction-0.3.p5/src
    %makeinstall_std
popd

#------------------------------------------------------------------------
rm -f %{buildroot}%{_bindir}/spkg-debian-maybe
pushd $SAGE_LOCAL/bin/
    # not supported - only prebuilt packages for now
    rm -f sage-{bdist,build,build-debian,clone,crap,debsource,download_package,env,libdist,location,make_devel_packages,omega,pkg,pkg-nocompress,pull,push,sdist,sbuildhack,upgrade}
    rm -f sage-list-* sage-mirror* SbuildHack.pm sage-test-*
    rm -f sage-{verify-pyc,hardcode_sage_root,check-64,spkg*,update*,starts}
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
    mkdir -p $SAGE_LOCAL/java
    pushd $SAGE_LOCAL/java
	rm -f jmol && ln -sf %{_datadir}/jmol jmol
    popd
popd

#------------------------------------------------------------------------
pushd spkg/build/graphs-20070722
    mkdir -p $SAGE_DATA/graphs
    cp -fa graphs/* $SAGE_DATA/graphs
popd

#------------------------------------------------------------------------
pushd spkg/build/polytopes_db-20080430
    mkdir -p $SAGE_DATA/reflexive_polytopes
    cp -fa reflexive_polytopes/* $SAGE_DATA/reflexive_polytopes
popd

#------------------------------------------------------------------------
if [ -d %{buildroot}%{_prefix}/dsage ]; then
    rm -fr $SAGE_LOCAL/dsage
    mv -f %{buildroot}%{_prefix}/dsage $SAGE_LOCAL
fi

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export CUR=\`pwd\`
export DOT_SAGE="\$HOME/.sage/"
mkdir -p \$DOT_SAGE
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_DATA="$SAGE_DATA"
export SAGE_DOC="$SAGE_DOC"
export PATH=$SAGE_LOCAL/bin:\$PATH
export SINGULARPATH=%{_datadir}/singular/LIB
export SINGULAR_BIN_DIR=%{_datadir}/singular/%{_arch}
%if %{use_sage_pexpect}
export PYTHONPATH="%{buildroot}%{SAGE_PYTHONPATH}"
%endif
export SAGE_CBLAS=cblas
$SAGE_LOCAL/bin/sage-sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
pushd spkg/build/jsmath-3.6b.p1
    cp -far src/jsmath $SAGE_LOCAL/notebook/javascript
    mkdir -p $SAGE_LOCAL/notebook/javascript/jsmath/fonts
    cp -far src/msbm10 $SAGE_LOCAL/notebook/javascript/jsmath/fonts
popd

pushd spkg/build/tinyMCE-3.2.0.2.p0
    cp -far src/tinymce/jscripts/tiny_mce $SAGE_LOCAL/notebook/javascript
popd

pushd spkg/build/jquery-1.2.6.p0
    cp -f patches/jquery.event.extendedclick.js src/jquery-plugins
    cp -far src/jquery $SAGE_LOCAL/notebook/javascript
    mkdir -p $SAGE_LOCAL/notebook/javascript/jquery/plugins
    cp -far src/jquery-plugins/* $SAGE_LOCAL/notebook/javascript/jquery/plugins
popd

pushd spkg/build/jqueryui-1.6r807svn.p0
    cp -far patches/sage patches/flora src/themes
    mkdir -p $SAGE_LOCAL/notebook/javascript/jqueryui
    cp -far src/*LICENSE.txt src/themes src/ui/minified/* \
	$SAGE_LOCAL/notebook/javascript/jqueryui
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
# fixup cython interface:
# o link with proper atlas
# o install csage headers
# o install .pxi and .pxd files
pushd spkg/build/sage-%{version}
    # make atlas/blas available to compiled sources
    perl -pi -e								\
	's|^(extra_link_args =).*|$1 ["-L%{_libdir}/atlas"]|;'		\
	%{buildroot}/%{py_platsitedir}/sage/misc/cython.py
    # make csage headers available
    mkdir -p %{buildroot}/%{_includedir}/csage
    cp -fa c_lib/include/* %{buildroot}/%{_includedir}/csage
    for f in `find sage \( -name \*.pxi -o -name \*.pxd \)`; do
	install -D -m 0644 $f %{buildroot}/%{py_platsitedir}/$f
    done
    # need this or will not "find" the files in the directory, and
    # fail to link with gmp
    # FIXME sagemath is no longer using gmp by default, but mpir
    # (licence issue, with gmp being gpl 3, and mpir gpl 2)
    touch %{buildroot}/%{py_platsitedir}/sage/libs/gmp/__init__.py
popd

#------------------------------------------------------------------------
# Build documentation, using %{buildroot} environment, as it needs
# to run and load sage python modules
pushd spkg/build/sage-%{version}/doc
    export DOT_SAGE=%{buildroot}/.sage
    export SAGE_DOC=`pwd`
    export PATH=%{buildroot}%{_bindir}:$SAGE_LOCAL/bin:$PATH
    export SINGULARPATH=%{_datadir}/singular/LIB
    export SINGULAR_BIN_DIR=%{_datadir}/singular/%{_arch}
    export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
    export PYTHONPATH=%{buildroot}%{py_platsitedir}
    # there we go
    python common/builder.py all html
    export SAGE_DOC=%{buildroot}%{SAGE_DOC}
    cp -far output $SAGE_DOC
    # some "user setup" files will be installed there...
    rm -fr $DOT_SAGE
popd

# Script was used to build documentation 
perl -pi -e 's|%{buildroot}||g;' %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
# Fixup links
rm -fr $SAGE_DEVEL/sage $SAGE_DATA/extcode/sage
ln -sf %{py_platsitedir} $SAGE_DEVEL/sage
ln -sf %{py_platsitedir} $SAGE_DATA/extcode/sage
rm -f %{buildroot}%{py_platsitedir}/site-packages

########################################################################
%clean
# rm -rf #%#{buildroot}


########################################################################
%files
%defattr(-,root,root)
%dir %{py_platsitedir}/sage
%dir %{py_platsitedir}/dsage
%{py_platsitedir}/sage/*
%{py_platsitedir}/dsage/*
%{py_platsitedir}/*.egg-info
# MoinMoin extra files
%{py_platsitedir}/MoinMoin/macro/*
%{py_platsitedir}/MoinMoin/parser/*
%{_datadir}/moin/htdocs/jsmath
%dir %{SAGE_ROOT}
%{SAGE_ROOT}/*
%{_bindir}/*
%{_libdir}/*.so
%dir %{_includedir}/csage
%{_includedir}/csage/*
