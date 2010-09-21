# uncomment to DISABLE build of debug packages
#%#define		_enable_debug_packages	%{nil}
#%#define		debug_package		%{nil}

%define _requires_exceptions		perl(jQuery)

# Run "sage -testall" after building documentation?
%define		with_check		0
%define		SAGE_TIMEOUT		60
%define		SAGE_TIMEOUT_LONG	300

# duplicated mpmath from sympy causes serious problems now
# and python-mpmath should not be installed
%define		mpmath_from_sympy	1

# http://bugs.python.org/issue7689
%define		pickle_patch		1

%define		name			sagemath
%define		SAGE_ROOT		%{_datadir}/sage
%define		SAGE_LOCAL		%{SAGE_ROOT}/local
%define		SAGE_DEVEL		%{SAGE_ROOT}/devel
%define		SAGE_DOC		%{SAGE_DEVEL}/doc
%define		SAGE_DATA		%{SAGE_ROOT}/data

# Need this because as of sage 4.0.1, it only works "correctly" with python-pexpect 2.0
%define		use_sage_pexpect	1

# python-networkx currently broken at least in x86_64 (and needs a patch for sage)
%define		use_sage_networkx	1

%define		SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	4.5.3
Release:	%mkrel 1
Source0:	http://www.sagemath.org/src/sage-%{version}.tar
Source1:	moin-1.9.1-filesystem.tar.bz2
Source2:	sets.py
Source3:	makecmds.sty
URL:		http://www.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#------------------------------------------------------------------------
%if %{with_check}
BuildRequires:	axiom
%endif

BuildRequires:	boost-devel

BuildRequires:	coin-or-devel

%if %{with_check}
BuildRequires:	cddlib-devel
%endif

BuildRequires:	cliquer-devel
BuildRequires:	dos2unix
BuildRequires:	ecl
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel

%if %{with_check}
BuildRequires:	eclib-mwrank
%endif

BuildRequires:	flex bison
BuildRequires:	flint-devel
BuildRequires:	fplll-devel
BuildRequires:	gap-system

%if %{with_check}
BuildRequires:	gap-system-packages
%endif

BuildRequires:	gcc-gfortran
BuildRequires:	gd-devel

%if %{with_check}
BuildRequires:	gfan
%endif

BuildRequires:	givaro-devel
BuildRequires:	glpk-devel

%if %{with_check}
BuildRequires:	gp2c pari pari-data
%endif

BuildRequires:	gsl-devel
BuildRequires:	iml
BuildRequires:	ipython

BuildRequires:	lcalc-devel
BuildRequires:	libatlas-devel
BuildRequires:	libblas-devel
BuildRequires:	libgmpxx-devel
BuildRequires:	libm4ri-devel
BuildConflicts:	libm4ri-static-devel
BuildRequires:	libpari-devel
BuildRequires:	libxml2-devel
BuildRequires:	linalg-linbox-devel

%if %{with_check}
BuildRequires:	macaulay2
BuildRequires:	maxima-runtime
%endif

BuildRequires:	mpfi-devel
BuildConflicts:	mpfi-static-devel
BuildRequires:	ntl-devel

%if %{with_check}
BuildRequires:	octave
BuildRequires:	palp
%endif

BuildRequires:	png-devel
BuildRequires:	polybori
BuildRequires:	polybori-devel
BuildConflicts:	polybori-static-devel

%if %{with_check}
BuildRequires:	polymake
%endif

BuildRequires:	pynac-devel

%if %{with_check}
BuildRequires:	python-cvxopt
%endif

BuildRequires:	python-cython
BuildRequires:	python-jinja2

BuildRequires:	python-matplotlib
BuildRequires:	python-matplotlib-gtk
%if !%{mpmath_from_sympy}
BuildRequires:	python-mpmath
%endif

%if %{with_check}
  %if !%{use_sage_networkx}
BuildRequires:	python-networkx
  %endif
%endif

BuildRequires:	python-numpy-devel

%if %{with_check}
  %if !%{use_sage_pexpect}
Requires:	python-pexpect
  %endif
BuildRequires:	python-polybori
%endif

%if %{with_check}
BuildRequires:	python-rpy python-rpy2
%endif

BuildRequires:	python-setuptools
BuildRequires:	python-scipy
BuildRequires:	python-sphinx

%if %{with_check}
BuildRequires:	python-sqlite2
BuildRequires:	python-sympy
%endif

BuildRequires:	python-twisted-core
BuildRequires:	python-twisted-web2
BuildRequires:	qd-static-devel

%if %{with_check}
BuildRequires:	python-zodb3
%endif

BuildRequires:	ratpoints

%if %{with_check}
BuildRequires:	R-base
%endif

BuildRequires:	readline-devel
BuildRequires:	scons
BuildRequires:	singular
BuildRequires:	singular-devel
BuildConflicts:	singular-static-devel
BuildRequires:	symmetrica-static-devel

%if %{with_check}
BuildRequires:	tachyon
%endif

BuildRequires:	tetex-latex

BuildRequires:	zn_poly-static-devel

#------------------------------------------------------------------------
Requires:	axiom
Requires:	bzip2
Requires:	cddlib-devel
Requires:	cliquer-devel
Requires:	ecl
Requires:	eclib-mwrank
Requires:	ecm
Requires:	flint
Requires:	fplll
Requires:	gap-system gap-system-packages
Requires:	gcc-gfortran
Requires:	gd-utils
Requires:	gfan
Requires:	gp2c pari pari-data libpari-devel
Requires:	ipython
Requires:	jmol

%ifarch %{ix86}
Suggests:	kant-kash
%endif

Requires:	lcalc

Requires:	libatlas
Requires:	libblas

# FIXME .a and .so files (this is also a sage specific library)
Requires:	libm4ri

# FIXME unversioned .so
Requires:	libeclib-devel

Requires:	libmpfi
Requires:	libopencdk

# currently in non-free due to lack of license information
Suggests:	lie

Requires:	linalg-linbox

Requires:	macaulay2

Requires:	maxima
Requires:	xmaxima

# Requires:	mercurial

Requires:	moin
Requires:	ntl-devel
Requires:	octave
Requires:	palp
Requires:	perl
Requires:	polybori
Requires:	polybori-devel
Requires:	polymake
Requires:	povray
Requires:	pynac-devel
Requires:	python
Requires:	python-cvxopt
Requires:	python-cython
Requires:	python-gd
Requires:	python-gnutls
Requires:	python-jinja2

%if !%{use_sage_networkx}
Requires:	python-networkx
%endif

Requires:	python-matplotlib

%if %{mpmath_from_sympy}
Conflicts:	python-mpmath
%else
Requires:	python-mpmath
%endif

Requires:	python-numpy

%if !%{use_sage_pexpect}
Requires:	python-pexpect
%endif

Requires:	python-polybori
Requires:	python-pycrypto
Requires:	python-pygments

Requires:	python-rpy python-rpy2

# scipy should also provide the weave (http://www.scipy.org/Weave) dependency
Requires:	python-scipy
Requires:	python-sphinx

Requires:	python-sqlite2
Requires:	python-sympy
Requires:	python-twisted-core
Requires:	python-twisted-web2

# FIXME only enough dependencies to run example.sage were added to distro
# see package url for information on other listed dependencies
Requires:	python-zodb3

%ifarch %{ix86}
Requires:	qepcad
%endif

Requires:	R-base
Requires:	scilab
Requires:	singular
Requires:	symmetrica
Requires:	sympow
Requires:	tachyon
Requires:	tetex-latex

#------------------------------------------------------------------------
Patch0:		sage-4.5.3.patch
Patch1:		sage-4.5.3-sage_scripts.patch
Patch2:		sage-4.5.3-wiki.patch
Patch3:		sage-4.5.3-qepcad.patch
Patch4:		sage-4.5.3-lie.patch
Patch5:		sage-4.5.3-sagedoc.patch
Patch6:		sage-4.5.3-list_plot.patch
Patch7:		sage-4.5.3-givaro.patch
Patch8:		sage-4.5.3-sagenb.patch
Patch9:		sage-4.5.3-gmp5.patch
Patch10:	sage-4.5.3-arpack.patch
Patch11:	sage-4.5.3-maxima.patch
Patch12:	sage-4.5.3-networkx.patch
Patch13:	sage-4.5.3-sympy_mpmath.patch

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
		elliptic_curves-0.1		\
		examples-%{version}		\
		extcode-%{version}		\
		flintqs-20070817.p5		\
		genus2reduction-0.3.p6		\
		graphs-20070722.p1		\
		polytopes_db-20100210		\
		rubiks-20070912.p12		\
		sage-%{version}			\
		sagenb-0.8.2			\
		sage_scripts-%{version}		\
		sagetex-2.2.5			\
%if %{pickle_patch}
		python-2.6.4.p9			\
%endif
    ; do
	tar jxf standard/$pkg.spkg -C build
    done
    rm -f build/sage_scripts-%{version}/*.orig

%if %{use_sage_pexpect}
    tar jxf standard/pexpect-2.0.p4.spkg -C build
%endif

%if %{use_sage_networkx}
    tar jxf standard/networkx-1.2.p1.spkg -C build
%endif
popd

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%if %{use_sage_networkx}
%patch12 -p1
%endif
%if %{mpmath_from_sympy}
%patch13 -p1
%endif

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
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
pushd spkg/build/genus2reduction-0.3.p6/src
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

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    # ensure proper/preferred libatlas is in linker path
    perl -pi -e 's|^(extra_link_args = ).*|$1\["-L%{_libdir}/atlas"\]|;' sage/misc/cython.py
    # some .c files are not (re)generated
    find . \( -name \*.pyx -o -name \*.pxd \) -exec touch {} \;
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
	CXX=g++ UNAME=Linux SAGE64=auto scons
    popd
    pushd sage/libs/mpmath
	dos2unix -U ext_impl.pxd ext_libmp.pyx ext_main.pxd ext_main.pyx
    popd
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/sagenb-0.8.2/src/sagenb
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/flintqs-20070817.p5/src
    %make CPP="g++ %{optflags} -fPIC"
popd

#------------------------------------------------------------------------
pushd spkg/build/genus2reduction-0.3.p6/src
    %make
popd

#------------------------------------------------------------------------
pushd spkg/build/rubiks-20070912.p12/src
    %make CC="gcc -fPIC" CXX="g++ -fPIC" CFLAGS="%{optflags}"
popd

#------------------------------------------------------------------------
%if %{pickle_patch}
    pushd spkg/build/python-2.6.4.p9/src
	cp ../patches/cPickle.c Modules/cPickle.c
	%configure
	perl -pi						\
	    -e 's|-Wl,--no-undefined||;'			\
	    Makefile
	%make
    popd
%endif


########################################################################
%install
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
export SAGE_DATA=%{buildroot}%{SAGE_DATA}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}
export SAGE_PYTHONPATH=%{buildroot}%{SAGE_PYTHONPATH}

export DESTDIR=%{buildroot}

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p $SAGE_PYTHONPATH
rm -fr $SAGE_DEVEL/sage $SAGE_LOCAL/{include,lib,share,notebook}
mkdir -p $SAGE_DATA $SAGE_DOC $SAGE_LOCAL $SAGE_DEVEL/sage
ln -sf %{_builddir}/sage-%{version}/spkg/build/sage-%{version}/sage $SAGE_DEVEL/sage/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
# "fix" most remaining doctest failures
cp -f %{SOURCE2} $SAGE_PYTHONPATH

#------------------------------------------------------------------------
# install moin changes
pushd %{buildroot}
    tar jxf %{SOURCE1}
popd

# make jsMath available to moin
mkdir -p %{buildroot}%{py_puresitedir}/MoinMoin/web/static/htdocs/common/js
rm -f %{buildroot}%{py_puresitedir}/MoinMoin/web/static/htdocs/common/js/jsmath
ln -sf %{SAGE_DEVEL}/sage/sagenb/data/jsmath %{buildroot}%{py_puresitedir}/MoinMoin/web/static/htdocs/common/js/jsmath

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
    pushd sage
	# install sage notebook templates
	cp -fa server/notebook/templates %{buildroot}%{py_platsitedir}/sage/server/notebook
    popd
    # install documentation sources
    rm -fr $SAGE_DOC/{common,en,fr}
    cp -far doc/{common,en,fr} $SAGE_DOC
popd

#------------------------------------------------------------------------
pushd spkg/build/sagenb-0.8.2/src/sagenb
    rm -f %{buildroot}%{py_platsitedir}/sagenb/data/jmol
    python setup.py install --root=%{buildroot} --install-purelib=%{py_platsitedir}
    # FIXME needs more then just path adjusting
    rm -f %{buildroot}%{_bindir}/sage3d
    # remove duplicated jmol (that only works with sage)
    rm -f %{buildroot}%{_bindir}/jmol
    rm -fr %{buildroot}%{py_platsitedir}/sagenb/data/jmol
    # and use system one
    ln -sf %{_datadir}/jmol %{buildroot}%{py_platsitedir}/sagenb/data/jmol
popd

#------------------------------------------------------------------------
%if %{use_sage_pexpect}
pushd spkg/build/pexpect-2.0.p4/src
    cp -f {ANSI,FSM,pexpect,pxssh,screen}.py $SAGE_PYTHONPATH
popd
%endif

#------------------------------------------------------------------------
%if %{use_sage_networkx}
pushd spkg/build/networkx-1.2.p1/src
    rm -fr $SAGE_PYTHONPATH/networkx*
    rm -fr %{buildroot}%{py_platsitedir}/networkx*
    python setup.py install --root=%{buildroot} --install-purelib=%{SAGE_PYTHONPATH}
    rm -fr $SAGE_DOC/networkx*
    mv -f %{buildroot}/%{_datadir}/doc/* $SAGE_DOC
    rmdir %{buildroot}/%{_datadir}/doc
popd
%endif

#------------------------------------------------------------------------
pushd spkg/build/sage_scripts-%{version}
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* *doctest.py ipy_profile_sage.py $SAGE_LOCAL/bin
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
pushd spkg/build/flintqs-20070817.p5/src
    cp -fa QuadraticSieve $SAGE_LOCAL/bin
popd

#------------------------------------------------------------------------
pushd spkg/build/genus2reduction-0.3.p6/src
    %makeinstall_std
popd

#------------------------------------------------------------------------
pushd spkg/build/rubiks-20070912.p12/src
    make DESTDIR=%{buildroot} PREFIX=%{SAGE_LOCAL} INSTALL=cp install
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
    cp -far			\
	gap			\
	genus2reduction		\
	gnuplot			\
	images			\
	kash			\
	macaulay2		\
	magma			\
	maple			\
	matlab			\
	mathematica		\
	maxima			\
	MuPAD			\
	mwrank			\
	notebook		\
	octave			\
	pari			\
	pickle_jar		\
	QEPCAD			\
	sagebuild		\
	scilab			\
	singular		\
	sobj			\
	$SAGE_DATA/extcode
popd

#------------------------------------------------------------------------
pushd spkg/build/graphs-20070722.p1
    mkdir -p $SAGE_DATA/graphs
    cp -fa graphs/* $SAGE_DATA/graphs
popd

#------------------------------------------------------------------------
pushd spkg/build/polytopes_db-20100210
    mkdir -p $SAGE_DATA/reflexive_polytopes
    cp -fa reflexive_polytopes/* $SAGE_DATA/reflexive_polytopes
popd

#------------------------------------------------------------------------
mkdir -p $SAGE_ROOT/examples
pushd spkg/build/examples-%{version}
    cp -far ajax calculus comm_algebra example.py example.sage finance \
	fortran gsl latex_embed linalg modsym programming \
	test_all tests worksheets \
	$SAGE_ROOT/examples
popd

#------------------------------------------------------------------------
pushd spkg/build/sagetex-2.2.5/src
    python setup.py install --root=%{buildroot} --install-purelib=%{py_platsitedir}
    install -m 0644 -D %{SOURCE3} \
	%{buildroot}%{_datadir}/texmf/tex/generic/sagetex/`basename %{SOURCE3}`
popd

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export CUR=\`pwd\`
##export DOT_SAGE="\$HOME/.sage/"
export DOT_SAGENB="\$DOT_SAGE"
mkdir -p \$DOT_SAGE/{maxima,sympow,tmp}
export SAGE_TESTDIR=\$DOT_SAGE/tmp
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_DATA="$SAGE_DATA"
export SAGE_DEVEL="$SAGE_DEVEL"
##export SAGE_DOC="$SAGE_DOC"
export PATH=$SAGE_LOCAL/bin:%{_datadir}/cdd/bin:\$PATH
export SINGULARPATH=%{_datadir}/singular/LIB
export SINGULAR_BIN_DIR=%{_datadir}/singular/%{_arch}
%if %{use_sage_pexpect}
##export PYTHONPATH="$SAGE_PYTHONPATH"
%endif
export SAGE_CBLAS=cblas
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=\`gfortran --print-file-name=libgfortran.so\`
export SYMPOW_DIR="\$DOT_SAGE/sympow"
$SAGE_LOCAL/bin/sage-sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

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
    # Big hack (tm)
    # when passing the full buildroot path, the pexpect interface fails
    # to communicate with gap, due to too long workspace pathname
    # (that is longer then 80 characters)
    # export DOT_SAGE=%{buildroot}/.sage
    export DOT_SAGE=/tmp/sage$$

    mkdir -p $DOT_SAGE/tmp
    export SAGE_DOC=`pwd`
    export PATH=%{buildroot}%{_bindir}:$SAGE_LOCAL/bin:%{_datadir}/cdd/bin:$PATH
    export SINGULARPATH=%{_datadir}/singular/LIB
    export SINGULAR_BIN_DIR=%{_datadir}/singular/%{_arch}
    export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
    export PYTHONPATH=%{buildroot}%{py_platsitedir}

    # there we go
    python common/builder.py all html
    export SAGE_DOC=%{buildroot}%{SAGE_DOC}
    cp -far output $SAGE_DOC


    #--------------------------------------------------------------------
%if %{with_check}
    %if %{use_sage_pexpect}
	cp -f $SAGE_PYTHONPATH/{ANSI,FSM,pexpect,pxssh,screen}.py %{buildroot}%{py_platsitedir}
    %endif

    %if %{use_sage_networkx}
	# move in buildroot because PYTHONPATH is already overriden
	mv -f %{buildroot}%{SAGE_PYTHONPATH}/networkx* %{buildroot}%{py_platsitedir}
    %endif

    # make sage-test checking of 'devel' prefix happy
    export SAGE_DOC=%{buildroot}%{SAGE_DOC}
    rm -f $SAGE_ROOT/doc

    SAGE_TIMEOUT=%{SAGE_TIMEOUT} SAGE_TIMEOUT_LONG=%{SAGE_TIMEOUT_LONG} sage -testall || :
    cp -f $DOT_SAGE/tmp/test.log $SAGE_DOC

    %if %{use_sage_pexpect}
	rm -f %{buildroot}%{py_platsitedir}/{ANSI,FSM,pexpect,pxssh,screen}.py
    %endif

    %if %{use_sage_networkx}
	# revert back to directory where it will be installed
	mv -f %{buildroot}%{py_platsitedir}/networkx* %{buildroot}%{SAGE_PYTHONPATH}
    %endif
%endif

    #--------------------------------------------------------------------
    # some "user setup" files will be installed there...
    rm -fr $DOT_SAGE
popd

#------------------------------------------------------------------------
# Script was used to build documentation 
perl -pi -e 's|%{buildroot}||g;s|^##||g;' %{buildroot}%{_bindir}/sage

%if %{pickle_patch}
    pushd spkg/build/python-2.6.4.p9/src
	install -m 0644 ../patches/pickle.py %{buildroot}%{SAGE_PYTHONPATH}
	cp `find . -name cPickle.so` %{buildroot}%{SAGE_PYTHONPATH}
    popd
%endif

#------------------------------------------------------------------------
# Fixup links
rm -fr $SAGE_DEVEL/sage $SAGE_DATA/extcode/sage $SAGE_ROOT/doc
ln -sf %{py_platsitedir} $SAGE_DEVEL/sage
ln -sf %{py_platsitedir} $SAGE_DATA/extcode/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
rm -f %{buildroot}%{py_platsitedir}/site-packages

# Install menu and icons
pushd spkg/build/extcode-%{version}
    install -m644 -D notebook/images/icon16x16.png %{buildroot}%{_miconsdir}/%{name}.png
    install -m644 -D notebook/images/icon32x32.png %{buildroot}%{_iconsdir}/%{name}.png
    install -m644 -D notebook/images/icon32x32.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
    install -m644 -D notebook/images/icon48x48.png %{buildroot}%{_liconsdir}/%{name}.png
popd
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Sagemath
Comment=A free open-source mathematics software system
Exec=sage
Icon=%{name}
Terminal=true
Type=Application
Categories=Science;Math;
EOF

########################################################################
%clean
# rm -rf #%#{buildroot}

########################################################################
# Update for sagetex and makecmds.sty added to it, so that can use tetex
%post
%{_bindir}/mktexlsr

%postun
%{_bindir}/mktexlsr

########################################################################
%files
%defattr(-,root,root)
%dir %{py_platsitedir}/sage
%dir %{py_platsitedir}/sagenb
%{py_platsitedir}/sage/*
%{py_platsitedir}/sagenb/*
%{py_platsitedir}/*.py
%{py_platsitedir}/*.egg-info
%{_datadir}/moin/data/plugin/action/*
%{_datadir}/moin/data/plugin/macro/*
%{_datadir}/moin/data/plugin/parser/*
%{py_puresitedir}/MoinMoin/web/static/htdocs/common/js/jsmath
%dir %{SAGE_ROOT}
%{SAGE_ROOT}/*
%{_bindir}/*
%{_libdir}/*.so
%dir %{_includedir}/csage
%{_includedir}/csage/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}*.png
%{_miconsdir}/%{name}*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_datadir}/texmf/tex/generic/sagetex
%{_datadir}/texmf/tex/generic/sagetex/*
