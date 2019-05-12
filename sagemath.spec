#%#define __noautoprov		'[^l][^i][^b]([-a-zA-Z_]+)\.so\(\)'
%define __noautoreq 'lib(s|t)atlas\\.so\\..\|pythonegg\(flask-oldsessions\).*'

%define _disable_lto 1
%define _disable_ld_no_undefined 1

%bcond_without bundled_ipython
%bcond_without bundled_pari
%bcond_without cython_hack
%bcond_without install_hack

%bcond_with docs

# not functional due to missing jar dependencies
%bcond_with sage3d

%bcond_without sphinx_hack

%ifarch %{x86_64}
%bcond_without fes
%else
%bcond_with fes
%endif

# set to run sage -testall in %%install
%global with_check		0
%global SAGE_TIMEOUT		60
%global SAGE_TIMEOUT_LONG	180

%global conway_polynomials_pkg	conway_polynomials-0.4
%global cysignals_pkg		cysignals-1.1.1
%global	elliptic_curves_pkg	elliptic_curves-0.8
%global	flintqs_pkg		flintqs-1.0
%global graphs_pkg		graphs-20151224
%if %{with bundled_ipython}
%global ipython_pkg		ipython-5.0.0
%endif
%if %{with bundled_pari}
%global pari_pkg		pari-2.8.0.alpha
%endif
%global pexpect_pkg		pexpect-4.1.0
%global polytopes_db_pkg	polytopes_db-20120220
%global rubiks_pkg		rubiks-20070912
%global	sagenb_pkg		sagenb-0.13
%global sagetex_pkg		sagetex-3.0

%global SAGE_ROOT		%{_libdir}/sagemath
%global SAGE_LOCAL		%{SAGE_ROOT}/local
%global SAGE_SRC		%{SAGE_ROOT}/src
%global SAGE_DOC		%{_docdir}/%{name}
%global SAGE_SHARE		%{_datadir}/sagemath
%global SAGE_ETC		%{SAGE_SHARE}/etc
%global SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		sagemath
Group:		Sciences/Mathematics
Summary:	A free open-source mathematics software system
Version:	8.7
Release:	1
# The file ${SAGE_ROOT}/COPYING.txt is the upstream license breakdown file
# Additionally, every $files section has a comment with the license name
# before files with that license
License:	ASL 2.0 and BSD and GPL+ and GPLv2+ and LGPLv2+ and MIT and Public Domain
URL:		http://www.sagemath.org
Source0:	http://files.sagemath.org/src/sage-%{version}.tar.gz
Source1:	gprc.expect
Source2:	makecmds.sty
# not installed by jmol package, use one in sagemath jmol spkg
Source3:	Jmol.js
Source4:	JmolHelp.html
# from jmol-12.3.27.p2 spkg
Source5:	testjava.sh
Source6:	%{name}.rpmlintrc

# Upstream uses mpir not gmp, but the rpm package is tailored to use gmp
Patch1:		%{name}-gmp.patch

# Set of patches to work with system wide packages
Patch2:		%{name}-scripts.patch

# remove call to not implemented sagemath "is_package_installed" interfaces
# need to package coin-or solver in fedora
# remove check for non free solvers
Patch4:		%{name}-extensions.patch

# helper to:
#	o respect a DESTDIR environment variable
#	o avoid double '//' in pathnames, what can confused debugedit & co
#	o minor change to help in incremental builds by avoiding rebuilding
#	  files
#	o do not assume there is an installed sagemath
Patch5:		%{name}-rpmbuild.patch

# build documentation in buildroot environment
Patch6:		%{name}-sagedoc.patch

# sage notebook rpm and system environment adjustments
Patch7:		%{name}-sagenb.patch

# do not attempt to create state files in system directories
Patch8:		%{name}-readonly.patch

# work with all maxima-runtime lisp backend packages
Patch11:	%{name}-maxima.patch

# execute 4ti2 programs in $PATH not in $SAGE_ROOT/local/bin
Patch12:	%{name}-4ti2.patch

# http://trac.sagemath.org/sage_trac/ticket/12992
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1317
Patch13:	%{name}-pari.patch

# use jmol itself to export preview images
# FIXME besides not using X and told so, fails if DISPLAY is not set
Patch17:	%{name}-jmol.patch

# only cremona mini database built and installed
# FIXME add a package with the full cremona database
# FIXME actually it should be already available in pari-elldata
Patch18:	%{name}-cremona.patch

# lrslib is a requires
Patch19:	%{name}-lrslib.patch

# nauty cannot be packaged due to license restrictions
# http://cs.anu.edu.au/~bdm/nauty/
# http://pallini.di.uniroma1.it/
Patch20:	%{name}-nauty.patch

# gap hap package not (yet) available
# http://www-gap.mcs.st-and.ac.uk/Packages/hap.html
Patch21:	%{name}-gap-hap.patch

# correct path to Lfunction include
Patch22:	%{name}-lcalc.patch

# Patch to enable cbc once review requests are done in Fedora
Patch23:	%{name}-cbc.patch

# Patch to enable libgap once review request is done in Fedora
Patch24:	%{name}-libgap.patch

# Patch to enable fes once review requests are done in Fedora
Patch25:	%{name}-fes.patch

# Side effect of using distro packages
# https://bugzilla.redhat.com/show_bug.cgi?id=974769
Patch28:	%{name}-sympy.patch

# Mandriva specific
Patch29:	%{name}-underlink.patch

Patch30:	sagemath-includes.patch

Patch31:	sagemath-arb.patch

Patch32:        sagemath-atlas.patch

Patch100:	sagemath-pkgconfig1.2.patch
Patch101:	sagemath-disable_gen.patch
Patch102:	sagemath-cython0.25.patch

BuildRequires:	4ti2
BuildRequires:	arb-devel
BuildRequires:	cddlib-devel
BuildRequires:	boost-devel
BuildRequires:	cliquer-devel
BuildRequires:	coin-or-Cbc-devel
BuildRequires:	cryptominisat-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	ecl
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	factory-devel
%if %{with fes}
BuildRequires:	fes-devel
%endif
BuildRequires:	flint-devel
BuildRequires:	fplll-devel
BuildRequires:	gap
BuildRequires:	GAPDoc
BuildRequires:	gap-character-tables
BuildRequires:	gap-libs
BuildRequires:	gap-sonata
BuildRequires:	gap-table-of-marks
BuildRequires:	gc-devel
BuildRequires:	gcc-gfortran
BuildRequires:	gd-devel
BuildRequires:	glpk-devel
BuildRequires:	gnutls-devel
BuildRequires:	gsl-devel
BuildRequires:	iml-devel
%if %{without bundled_ipython}
BuildRequires:	python2-ipython
%endif
BuildRequires:	lapack-devel
BuildRequires:	lcalc-devel
BuildRequires:	libatlas-devel
BuildRequires:	libfac-devel
BuildRequires:	libgap-devel
BuildRequires:	libmpc-devel
%if %{without bundled_pari}
BuildRequires:	libpari-devel
%endif
BuildRequires:	linalg-linbox-devel
BuildRequires:	lrcalc-devel
BuildRequires:	m4ri-devel
BuildRequires:	m4rie-devel
BuildRequires:	maxima-runtime-ecl
BuildRequires:	mpfi-devel
BuildRequires:	ntl-devel
BuildRequires:	planarity-devel
BuildRequires:	brial-devel
BuildRequires:	ppl-devel
BuildRequires:	pynac-devel
BuildRequires:	python2-cython
BuildRequires:	python2-devel
BuildRequires:	python2-flask-autoindex
BuildRequires:	python2-flask-babel
BuildRequires:	python2-flask-openid
BuildRequires:	python2-flask-silk
BuildRequires:	python2-matplotlib
BuildRequires:	python2-networkx
BuildRequires:	python2-numpy-devel
BuildRequires:	python2-pexpect
BuildRequires:	python2-pkgconfig
BuildRequires:	python2-scipy
BuildRequires:	python2-twisted
BuildRequires:	python2-pickleshare
BuildRequires:	python2-prompt_toolkit
BuildRequires:	python2-future
BuildRequires:	python2-sphinx
BuildRequires:	python-sphinx
BuildRequires:	R
BuildRequires:	ratpoints-devel
BuildRequires:	readline-devel
BuildRequires:	python2-rpy2
BuildRequires:	rw-devel
BuildRequires:	scons
BuildRequires:	singular
BuildRequires:	singular-devel
BuildRequires:	symmetrica-devel
BuildRequires:	texlive-dvipng
BuildRequires:	zn_poly-devel

Requires:	4ti2
Requires:	cddlib-devel
Requires:	ecl
Requires:	fonts-otf-stix
Requires:	gap
Requires:	GAPDoc
Requires:	gap-character-tables
Requires:	gap-sonata
Requires:	gap-table-of-marks
Requires:	gfan
Requires:	gp2c
Requires:	iml-devel
%if %{without bundled_ipython}
Requires:	python2-ipython
%endif
Requires:	java-plugin
Requires:	jmol
Requires:	jsmath-fonts
Requires:	libatlas
Requires:	libpari-devel
Requires:	lrslib
Requires:	maxima-gui
Requires:	maxima-runtime-ecl
Requires:	palp
Requires:	pari
Requires:	pari-data
Requires:	python-enum34
Requires:	python2-pycrypto
Requires:	python2-cvxopt
BuildRequires:	python2-cython
BuildRequires:	python2-docutils
Requires:	python2-flask-autoindex
Requires:	python2-flask-babel
Requires:	python2-flask-openid
Requires:	python2-flask-silk
Requires:	python2-future
Requires:	python2-matplotlib
Requires:	python2-networkx
Requires:	python2-parsing
Requires:	python2-pickleshare
Requires:	python2-prompt_toolkit
Requires:	python2-pathlib2
Requires:	python2-pexpect
Requires:	python2-backports_abc
Requires:	python2-backports-shutil_get_terminal_size
Requires:	python2-backports
Requires:	python2-traitlets
Requires:	python2-ipython_genutils
Requires:	python2-pygments
Requires:	python2-scipy
Requires:	python2-simplegeneric
Requires:	python2-sympy
Requires:	python2-twisted
Requires:	R
Requires:	%{name}-core
Requires:	%{name}-data
%if %{with docs}
Requires:	%{name}-doc-en
%endif
Requires:	%{name}-notebook
Requires:	%{name}-rubiks
Requires:	%{name}-sagetex
Requires:	singular
Requires:	sympow
Requires:	tachyon
Requires:	texlive
Requires:	vecmath

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.

#------------------------------------------------------------------------
%package	core
Summary:	Open Source Mathematics Software
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	core
This package contains the core sagemath python modules.

#------------------------------------------------------------------------
%package	data
Summary:	Databases and scripts for %{name}
Group:		Sciences/Mathematics
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-data-conway_polynomials = %{version}-%{release}
Requires:	%{name}-data-elliptic_curves = %{version}-%{release}
Requires:	%{name}-data-etc = %{version}-%{release}
Requires:	%{name}-data-graphs = %{version}-%{release}
Requires:	%{name}-data-polytopes_db = %{version}-%{release}
BuildArch:	noarch

%description	data
Collection of databases and interface customization scripts for sagemath.

#------------------------------------------------------------------------
%package	data-conway_polynomials
Summary:	Conway Polynomials Database
Group:		Sciences/Mathematics
Requires:	%{name}-data = %{version}-%{release}
BuildArch:	noarch

%description	data-conway_polynomials
Small database of Conway polynomials for sagemath.

#------------------------------------------------------------------------
%package	data-elliptic_curves
Summary:	Databases of elliptic curves
Group:		Sciences/Mathematics
Requires:	%{name}-data = %{version}-%{release}
BuildArch:	noarch

%description	data-elliptic_curves
Includes two databases:

 * A small subset of the data in John Cremona's database of elliptic curves up
   to conductor 10000. See http://www.warwick.ac.uk/~masgaj/ftp/data/ or
   http://sage.math.washington.edu/cremona/INDEX.html

 * William Stein's database of interesting curves

#------------------------------------------------------------------------
%package	data-etc
Summary:	Extcode for Sagemath
Group:		Sciences/Mathematics
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:      %{name}-data-extcode < %{version}
BuildArch:	noarch

%description	data-etc
Collection of scripts and interfaces to sagemath.

#------------------------------------------------------------------------
%package	data-graphs
Summary:	Sagemath database of graphs
Group:		Sciences/Mathematics
Requires:	%{name}-data = %{version}-%{release}
BuildArch:	noarch

%description	data-graphs
A database of graphs. Created by Emily Kirkman based on the work of Jason
Grout. Since April 2012 it also contains the ISGCI graph database.

#------------------------------------------------------------------------
%package	data-polytopes_db
Summary:	Lists of 2- and 3-dimensional reflexive polytopes
Group:		Sciences/Mathematics
Requires:	%{name}-data = %{version}-%{release}
BuildArch:	noarch

%description	data-polytopes_db
The list of polygons is quite easy to get and it has been known for a while.
The list of 3-polytopes was originally obtained by Maximilian Kreuzer and
Harald Skarke using their software PALP, which is included into the standard
distribution of Sage. To work with lattice and reflexive polytopes from Sage
you can use sage.geometry.lattice_polytope module, which relies on PALP for
some of its functionality. To get access to the databases of this package, use
ReflexivePolytope and ReflexivePolytopes commands.

#------------------------------------------------------------------------
%package	doc
Summary:	Documentation infrastructure files for %{name}
Group:		Sciences/Mathematics
BuildArch:	noarch

%description	doc
This package contains the documentation infrastructure for %{name}.

#------------------------------------------------------------------------
%package	doc-de
Summary:	German documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-de
This package contains the German %{name} documentation.

#------------------------------------------------------------------------
%package	doc-en
Summary:	English documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-en
This package contains the English %{name} documentation.

#------------------------------------------------------------------------
%package	doc-fr
Summary:	French documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-fr
This package contains the French %{name} documentation.

#------------------------------------------------------------------------
%package	doc-pt
Summary:	Portuguese documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-pt
This package contains the Portuguese %{name} documentation.

#------------------------------------------------------------------------
%package	doc-ru
Summary:	Russian documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-ru
This package contains the Russian %{name} documentation.

#------------------------------------------------------------------------
%package	doc-tr
Summary:	Turkish documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc = %{version}-%{release}
BuildArch:	noarch

%description	doc-tr
This package contains the Turkish %{name} documentation.

#------------------------------------------------------------------------
%package	notebook
Summary:	The Sage Notebook
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	notebook
The Sage Notebook is a web-based graphical user interface for
mathematical software.

#------------------------------------------------------------------------
%package	rubiks
Summary:	Several programs for working with Rubik's cubes
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	rubiks
Several programs for working with Rubik's cubes, by three  different people.
In summary the three contributors are:

Michael Reid (GPL) http://www.math.ucf.edu/~reid/Rubik/optimal_solver.html
    optimal - uses many pre-computed tables to find an optimal 
              solution to the 3x3x3 Rubik's cube

Dik T. Winter (MIT License)
    cube    - uses Kociemba's algorithm to iteratively find a short
              solution to the 3x3x3 Rubik's cube 
    size222 - solves a 2x2x2 Rubik's cube 

Eric Dietz (GPL) http://www.wrongway.org/?rubiksource
    cu2   - A fast, non-optimal 2x2x2 solver
    cubex - A fast, non-optimal 3x3x3 solver
    mcube - A fast, non-optimal 4x4x4 solver

#------------------------------------------------------------------------
%package	sagetex
Summary:	Sagemath into LaTeX documents
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	sagetex
This is the SageTeX package. It allows you to embed code, results of
computations, and plots from the Sage mathematics software suite
(http://sagemath.org) into LaTeX documents.

########################################################################
%prep
%setup -q -n sage-%{version}

pushd build/pkgs/cysignals
    tar jxf ../../../upstream/%{cysignals_pkg}.tar.bz2
    mv %{cysignals_pkg} src
popd

pushd build/pkgs/conway_polynomials
    tar jxf ../../../upstream/%{conway_polynomials_pkg}.tar.bz2
    mv %{conway_polynomials_pkg} src
popd

pushd build/pkgs/elliptic_curves
    tar jxf ../../../upstream/%{elliptic_curves_pkg}.tar.bz2
    mv %{elliptic_curves_pkg} src
popd

pushd build/pkgs/flintqs
    tar jxf ../../../upstream/%{flintqs_pkg}.tar.bz2
    mv %{flintqs_pkg} src
    pushd src
	for diff in `ls ../patches/*.patch`; do
	    patch -p1 < $diff
	done
    popd
popd

pushd build/pkgs/graphs
    tar jxf ../../../upstream/%{graphs_pkg}.tar.bz2
    mv %{graphs_pkg} src
popd

%if %{with bundled_ipython}
pushd build/pkgs/ipython
    tar zxf ../../../upstream/%{ipython_pkg}.tar.gz
    mv %{ipython_pkg} src
popd
%endif

%if %{with bundled_pari}
pushd build/pkgs/pari
    tar zxf ../../../upstream/%{pari_pkg}.tar.gz
    mv %{pari_pkg} src
    pushd src
	for diff in ../patches/*.patch; do
	    patch -p1 < $diff
	done
	# Temporary workaround: redefining GCC_VERSION kills the build
	sed -i 's/GCC_VERSION/PARI_&/' config/paricfg.h.SH
    popd
popd
%endif

pushd build/pkgs/pexpect
    tar jxf ../../../upstream/%{pexpect_pkg}.tar.gz
    mv %{pexpect_pkg} src
    pushd src
	for diff in `ls ../patches/*.patch`; do
	    patch -p1 < $diff
	done
    popd
popd

pushd build/pkgs/polytopes_db
    tar jxf ../../../upstream/%{polytopes_db_pkg}.tar.bz2
    mv %{polytopes_db_pkg} src
popd

pushd build/pkgs/rubiks
    tar jxf ../../../upstream/%{rubiks_pkg}.tar.bz2
    mv %{rubiks_pkg} src
#    pushd src
#	cp ../patches/dietz-mcube-Makefile dietz/mcube/Makefile
#	cp ../patches/dietz-solver-Makefile dietz/solver/Makefile
#	cp ../patches/dietz-cu2-Makefile dietz/cu2/Makefile
#	cp ../patches/reid-Makefile reid/Makefile
#    popd
popd

pushd build/pkgs/sagenb
    tar xf ../../../upstream/%{sagenb_pkg}.tar.bz2
    mv %{sagenb_pkg} src
popd

pushd build/pkgs/sagetex
    tar jxf ../../../upstream/%{sagetex_pkg}.tar.gz
    mv %{sagetex_pkg} src
popd

%patch1
%patch2
%patch4
%patch5
%patch6
%patch7
%patch8
%patch11
%patch12
%if %{without bundled_pari}
%patch13
%endif

%patch17
%patch18
%patch19

%patch20
%patch21
%patch22

# other coin-or packages are build requires or coin-or-Cbc
%patch23

%patch24

%if %{without fes}
%patch25
%endif

%patch28
#patch29
%patch30
%patch31

%patch100 -p1
%patch101 -p1
%patch102 -p1

%patch32

sed -e 's|@@SAGE_ROOT@@|%{SAGE_ROOT}|' \
    -e 's|@@SAGE_DOC@@|%{SAGE_DOC}|' \
    -i src/sage/env.py

sed -e 's|@@CYSIGNALS@@|%{_builddir}%{python2_sitearch}/cysignals|' \
    -i src/setup.py

sed -e "s|'flask-oldsessions>=0.10',||" \
    -e "s|'http://github.com/mitsuhiko/flask-oldsessions/tarball/master#egg=flask-oldsessions-0.10'||" \
    -i build/pkgs/sagenb/src/setup.py

#------------------------------------------------------------------------
# ensure proper/preferred libatlas is in linker path
perl -pi -e 's|^(extra_link_args = ).*|$1\["-L%{_libdir}/atlas"\]|;' src/sage/misc/cython.py
%if 0%{?fedora} > 20
perl -pi -e "s|return 'atlas'|return 'satlas'|;" src/sage/misc/cython.py
%endif
# some .c files are not (re)generated
find src/sage \( -name \*.pyx -o -name \*.pxd \) | xargs touch

# remove bundled jar files before build
rm build/pkgs/sagenb/src/sagenb/data/sage3d/lib/sage3d.jar

# remove binary egg
rm -r build/pkgs/sagenb/src/sagenb.egg-info

# fix Singular paths
sed -e "s,SINGULARPATH=\",&%{_libdir}/Singular/LIB:," \
    -e "s,\(SINGULAR_EXECUTABLE=\"\).*\",\1%{_libdir}/Singular/Singular\"," \
    -i src/bin/sage-env

rm -f src/sage/misc/darwin*

sed -e 's|/usr/bin/env python|%__python2|' -i src/bin/*
########################################################################
%build
export CC=gcc
export CFLAGS="%{optflags} -fuse-ld=bfd -fno-lto"
export CXXFLAGS="%{optflags} -fuse-ld=bfd -fno-lto"
export LIBS="-lm -ldl"
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
# Avoid buildroot in gcc command line (use _builddir instead)
export SAGE_SRC="$PWD/src"
export SAGE_INC=%{_includedir}
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`
export DESTDIR=%{buildroot}
# Use file in /tmp because there are issues with long pathnames
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

# Avoid surprises due to change to src/build/temp.*$ARCH.*/...
export SAGE_CYTHONIZED=$SAGE_SRC/build/cythonized

# match system packages as sagemath packages
rm -Rf $SAGE_LOCALE $SAGE_ROOT
mkdir -p $SAGE_ROOT $SAGE_LOCAL
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

mkdir bin; pushd bin; ln -s /usr/bin/ld.bfd ld; popd
export PATH=$PWD/bin:%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python2_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
# Save and update environment to generate bundled interfaces
save_PATH=$PATH
save_LOCAL=$SAGE_LOCAL
export PATH=%{_builddir}/bin:$PATH
export SAGE_LOCAL=%{_builddir}

%if %{with bundled_ipython}
pushd build/pkgs/ipython/src
    %__python2 setup.py build
    %__python2 setup.py install --root %{_builddir}
popd
%endif

%if %{with bundled_pari}
# Build bundled pari-2.8
pushd build/pkgs/pari/src
    ./Configure --prefix=%{_builddir} \
	--without-readline --with-gmp \
	--kernel=gmp --graphic=none
    sed -i 's|%{_builddir}|%{_prefix}|g' Olinux-*/paricfg.h
    make %{?_smp_mflags} gp
    make install DESTDIR=""
    cp -p src/language/anal.h  %{_builddir}/include/pari/anal.h
popd
%endif

# Generate pari interface
pushd src
    %__python2 -c "from sage_setup.autogen.interpreters import rebuild; rebuild('sage/ext/interpreters')"
    %__python2 -c "from sage_setup.autogen.pari import rebuild; rebuild()"
popd

%if %{with bundled_pari}
# Make temporary headers and static library visible
sed -i 's|\(^    include_directories = \[SAGE_INC,\)|\1 "%{_builddir}/include",|' \
    src/sage/env.py
sed -i 's|\(^extra_link_args = \[\) \]|\1"-L%{_builddir}/lib"\]|' \
    src/setup.py
sed -i 's|m.library_dirs + |m.library_dirs + ["%{_builddir}/lib"] + |' \
    src/setup.py
%endif

pushd build/pkgs/cysignals/src
    %__python2 setup.py build
    %__python2 setup.py install --root %{_builddir}
popd

export PYTHONPATH=%{_builddir}%{python2_sitearch}:$PYTHONPATH

%if %{with cython_hack}
    cp -far %{python2_sitearch}/Cython %{_builddir}%{python2_sitearch}
    PATCH=$PWD/build/pkgs/cython/patches/pxi_sys_path.patch
    pushd %{_builddir}%{python2_sitearch}
	patch -p1 < $PATCH
	# https://bugzilla.redhat.com/show_bug.cgi?id=1406533
	sed -i 's/disallow/dissallow/' Cython/Compiler/Options.py
    popd
%endif

# Restore environment used to generate bundled interfaces
export PATH=$save_PATH
export SAGE_LOCAL=$save_LOCAL
#------------------------------------------------------------------------
pushd src
    %__python2 -u ./setup.py build build_ext -lm,dl
popd

#------------------------------------------------------------------------
pushd build/pkgs/sagenb/src
    %__python2 ./setup.py build
popd

#------------------------------------------------------------------------
pushd build/pkgs/flintqs/src
    %configure
    make %{?_smp_mflags} CPP="g++ %{optflags} -fPIC"
popd

pushd build/pkgs/rubiks/src
    make %{?_smp_mflags} CC="gcc -fPIC" CXX="g++ -fPIC" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
popd

# Remove buildroot reference from cython comments
perl -pi -e 's|%{buildroot}||g;' `find src/build/cythonized -type f`

# Try hard to remove buildroot from binaries
rm -f `grep -lr "%{buildroot}" src/build/lib.linux-*/`
rm -f `grep -lr "%{buildroot}" src/build/temp.linux-*/`
pushd src
    %__python2 ./setup.py build build_ext -lm,dl
popd

# last build command
rm -fr $DOT_SAGE

########################################################################
%install
export CC=gcc
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
# Avoid buildroot in gcc command line (use _builddir instead)
export SAGE_SRC="$PWD/src"
export SAGE_INC=%{_includedir}
#export SAGE_SRC=#%#{buildroot}#%#{SAGE_SRC}
export SAGE_SHARE=%{buildroot}%{SAGE_SHARE}
export SAGE_ETC=%{buildroot}%{SAGE_ETC}
export SAGE_EXTCODE=%{buildroot}%{SAGE_ETC}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}
export SAGE_PYTHONPATH=%{buildroot}%{SAGE_PYTHONPATH}
%if %{with bundled_pari}
export LD_LIBRARY_PATH=%{_builddir}/lib:$LD_LIBRARY_PATH
%endif
export DESTDIR=%{buildroot}
export SAGE_DEBUG=no
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python2_sitearch}:$PYTHONPATH
export PYTHONPATH=%{_builddir}%{python2_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p $SAGE_PYTHONPATH
rm -fr $SAGE_LOCAL/{include,lib,share,notebook}
mkdir -p $SAGE_SHARE $SAGE_DOC $SAGE_LOCAL/bin %{buildroot}%{SAGE_SRC}
ln -sf $PWD/src/sage %{buildroot}%{SAGE_SRC}/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
pushd build/pkgs/cysignals/src
    pushd docs
	%__make html
    popd
    %__python2 setup.py install --root %{buildroot}
    mv %{buildroot}%{_bindir}/cysignals* $SAGE_LOCAL/bin
popd

#------------------------------------------------------------------------
pushd src/ext
    mkdir -p $SAGE_ETC
    for dir in 			\
	gap			\
	graphs			\
	images			\
	magma			\
	mwrank			\
	notebook-ipython; do
	COUNT=`find $dir -type f | wc -l `
	if [ $COUNT -gt 0 ]; then
	    cp -far $dir $SAGE_ETC
	fi
	cp -far pari $SAGE_ETC
    done
    cp -fa %{SOURCE1} $SAGE_ETC
popd

#------------------------------------------------------------------------
pushd src
%if %{without install_hack}
    # FIXME tries to rebuild everything
    %__python2 -u setup.py install --root=%{buildroot}
%else
    mkdir -p %{buildroot}%{python2_sitearch}
    cp -far build/lib.linux-*/sage %{buildroot}%{python2_sitearch}
%endif
%if %{with docs}
    # install documentation sources
    rm -fr $SAGE_DOC/{common,en,fr}
    cp -far doc/{common,ca,de,en,fr,hu,it,pt,ru,tr} $SAGE_DOC
%endif
popd

%if %{with bundled_pari}
# Revert change to make temporary headers and static library visible
# Making it search for the installed sagemath path
sed -i 's|\(^    include_directories = \[SAGE_INC,\).*|\1|' \
    %{buildroot}%{SAGE_SRC}/sage/env.py
%endif

#------------------------------------------------------------------------
pushd build/pkgs/sagenb/src
    rm -f %{buildroot}%{python2_sitearch}/sagenb/data/sage3d/sage3d
    %__python2 setup.py install --root=%{buildroot} --install-purelib=%{python2_sitearch}
    # jsmol
    ln -sf %{_jsdir}/jsmol $SAGE_SHARE/jsmol
    # sage3d
    rm -f %{buildroot}%{_bindir}/sage3d
%if %{with sage3d}
    ln -sf %{SAGE_LOCAL}/bin/sage3d %{buildroot}%{python2_sitearch}/sagenb/data/sage3d/sage3d
%endif
    ln -sf %{python2_sitearch}/sagenb %{buildroot}%{SAGE_SRC}/sagenb
    # use system mathjax
    ln -sf %{_jsdir}/mathjax %{buildroot}%{python2_sitearch}/sagenb/data/mathjax
popd

#------------------------------------------------------------------------
%if %{with bundled_pexpect}
pushd build/pkgs/pexpect/src
    cp -fa pexpect $SAGE_PYTHONPATH
popd
%endif

#------------------------------------------------------------------------
cp -fa COPYING.txt $SAGE_ROOT
pushd src/bin
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* $SAGE_LOCAL/bin
    pushd $SAGE_LOCAL/bin
	ln -sf %{_bindir}/jmol jmol
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/python2 python
%if %{without bundled_pari}
	ln -sf %{_bindir}/gp sage_pari
%endif
	ln -sf %{_bindir}/gap gap_stamp
	ln -sf %{_bindir}/ecm ecm
    popd
popd
install -p -m755 src/bin/sage $SAGE_LOCAL/bin

#------------------------------------------------------------------------
pushd build/pkgs/flintqs/src
    cp -fa src/QuadraticSieve $SAGE_LOCAL/bin
popd

pushd build/pkgs/rubiks/src
    cp -fa \
	reid/optimal \
	dietz/solver/cubex \
	dietz/mcube/mcube \
	dietz/cu2/cu2 \
	dik/dikcube \
	dik/size222 \
	$SAGE_LOCAL/bin
popd

#------------------------------------------------------------------------
pushd $SAGE_LOCAL/bin/
    for file in \
	sage-arch-env \
	sage-bdist \
	sage-build \
	sage-clone \
	sage-clone-source \
	sage-combinat \
	sage-crap \
	sage-dev \
	sage-download-file \
	sage-download-upstream \
	sage-env \
	sage-fix-pkg-checksums \
	sage-list-experimental \
	sage-list-optional \
	sage-list-packages \
	sage-list-standard \
	sage-location \
	sage-omega \
	sage-open \
	sage-pkg \
	sage-pull \
	sage-push \
	sage-pypkg-location \
	sage-README-osx.txt \
	sage-rebaseall.bat \
	sage-rebaseall.sh \
	sage-rebase.bat \
	sage-rebase.sh \
	sage-rebase \
	sage-rsyncdist \
	sage-sdist \
	sage-spkg \
	sage-starts \
	sage-sync-build.py \
	sage-test-import \
	sage-update-src \
	sage-update-version \
	sage-upgrade \
	spkg-install; do
	rm -f $file
    done
popd

#------------------------------------------------------------------------
pushd build/pkgs/conway_polynomials
    %__python2 ./spkg-install
popd

#------------------------------------------------------------------------
pushd build/pkgs/elliptic_curves
    # --short-circuit -bi debug build helper
    if [ ! -e src/ellcurves ]; then
	rm -fr src
	tar jxf ../../../upstream/%{elliptic_curves_pkg}.tar.bz2
	mv %{elliptic_curves_pkg} src
    fi
    %__python2 ./spkg-install
popd

#------------------------------------------------------------------------
pushd build/pkgs/graphs
    mkdir -p $SAGE_SHARE/graphs
    cp -fa src/* $SAGE_SHARE/graphs
popd

#------------------------------------------------------------------------
pushd build/pkgs/polytopes_db
    mkdir -p $SAGE_SHARE/reflexive_polytopes
    cp -fa src/* $SAGE_SHARE/reflexive_polytopes
popd

#------------------------------------------------------------------------
pushd build/pkgs/sagetex/src
    %__python2 setup.py install --root=%{buildroot} --install-purelib=%{python2_sitearch}
    install -p -m 0644 -D %{SOURCE2} \
	%{buildroot}%{_datadir}/texmf/tex/latex/sagetex/makecmds.sty
    mv %{buildroot}%{_datadir}/texmf/tex/latex/sagetex/CONTRIBUTORS \
	 %{buildroot}%{_docdir}/sagetex
    for file in PKG-INFO README; do
	install -p -m 0644 $file %{buildroot}%{_docdir}/sagetex/$file
    done
popd

#------------------------------------------------------------------------
%if %{with bundled_ipython}
mv %{_builddir}%{python2_sitelib}/IPython %{buildroot}%{SAGE_PYTHONPATH}
mv %{_builddir}%{_bindir}/ip* %{buildroot}%{SAGE_LOCAL}/bin
%endif

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/bash -i

export CUR=\`pwd\`
##export DOT_SAGE="\$HOME/.sage"
mkdir -p \$DOT_SAGE/{maxima,sympow,tmp}
export SAGE_TESTDIR=\$DOT_SAGE/tmp
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_SHARE="$SAGE_SHARE"
export SAGE_EXTCODE="$SAGE_ETC"
export SAGE_ETC="$SAGE_ETC"
export SAGE_SRC="%{buildroot}%{SAGE_SRC}"
##export SAGE_DOC="$SAGE_DOC"
##export SAGE_DOC_SRC="\$SAGE_DOC"
module load 4ti2-%{_arch}
module load lrcalc-%{_arch}
module load surf-%{_arch}
export PATH=$SAGE_LOCAL/bin:\$PATH
export SINGULARPATH=%{_libdir}/Singular/LIB
export SINGULAR_BIN_DIR=%{_libdir}/Singular
##export PYTHONPATH="$SAGE_PYTHONPATH:\$SAGE_LOCAL/bin"
export SAGE_CBLAS=blas
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=\`gfortran --print-file-name=libgfortran.so\`
export SYMPOW_DIR="\$DOT_SAGE/sympow"
export LC_MESSAGES=C
export LC_NUMERIC=C
export LD_LIBRARY_PATH=\$SAGE_ROOT/lib:\$LD_LIBRARY_PATH
# Required for sage -gdb
export SAGE_DEBUG=no
$SAGE_LOCAL/bin/sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
%if %{with sage3d}
cat > %{buildroot}%{SAGE_LOCAL}/bin/sage3d << EOF
#!/bin/sh

java -classpath %{SAGE_SRC}/sage/sagenb/data/sage3d/lib/sage3d.jar:%{_javadir}/j3dcore.jar:%{_javadir}/vecmath.jar:%{_javadir}/j3dutils.jar org.sagemath.sage3d.ObjectViewerApp "\$1"
EOF
chmod +x %{buildroot}%{SAGE_LOCAL}/bin/sage3d
%endif

#------------------------------------------------------------------------
# adjust cython interface:
# o install csage headers
# o install .pxi and .pxd files
pushd src
    for f in `find sage \( -name \*.pxi -o -name \*.pxd -o -name \*.pyx \)`; do
	install -p -D -m 0644 $f %{buildroot}%{python2_sitearch}/$f
    done
    # need this or will not "find" the files in the directory, and
    # fail to link with gmp
    touch %{buildroot}%{python2_sitearch}/sage/libs/gmp/__init__.py
popd

%if %{with docs}
#------------------------------------------------------------------------
%if %{with bundled_pexpect}
cp -fa $SAGE_PYTHONPATH/pexpect %{buildroot}%{python2_sitearch}
%endif

# Build documentation, using %#{buildroot} environment
export SAGE_SETUP=$PWD/src/sage_setup
pushd src/doc
    export SAGE_DOC=`pwd`
    export PATH=%{buildroot}%{_bindir}:$SAGE_LOCAL/bin:$PATH
    export SINGULARPATH=%{_libdir}/Singular/LIB
    export SINGULAR_BIN_DIR=%{_libdir}/Singular
    export LD_LIBRARY_PATH=%{_libdir}/atlas:$LD_LIBRARY_PATH
    export PYTHONPATH=$SAGE_SETUP:%{buildroot}%{python2_sitearch}:$SAGE_PYTHONPATH:$SAGE_DOC

%if %{with sphinx_hack}
    cp -far %{python2_sitelib}/sphinx %{buildroot}%{python2_sitearch}
    sed -i "s|\(source.startswith('>>>')\)|\1 or source.startswith('sage: ')|" \
	%{buildroot}%{python2_sitearch}/sphinx/highlighting.py
%endif

    # there we go
    ln -sf %{buildroot}%{SAGE_DOC} %{buildroot}%{SAGE_SRC}/doc
    export SAGE_DOC=%{buildroot}%{SAGE_DOC}
    export SAGE_DOC_SRC=$SAGE_DOC
    # python -m sage_setup.docbuild
    # FIXME there is a 'ja' translation, but adding it to $LANGUAGES
    # does not get documentation built
    LANGUAGES="ca de en fr hu it pt ru tr" \
	%__python2 -m docbuild --no-pdf-links -k all html
    rm -f %{buildroot}%{SAGE_SRC}/doc
    ln -sf %{SAGE_DOC} %{buildroot}%{SAGE_SRC}/doc

    # should not be required and encodes buildroot
    rm -fr $SAGE_DOC/output/doctrees
popd

%if %{with check}
export SAGE_TIMEOUT=%{SAGE_TIMEOUT}
export SAGE_TIMEOUT_LONG=%{SAGE_TIMEOUT_LONG}
sage -testall --verbose || :
install -p -m644 $DOT_SAGE/tmp/test.log $SAGE_DOC/test.log
# remove buildroot references from test.log
sed -i 's|%{buildroot}||g' $SAGE_DOC/test.log
%endif

%if %{with bundled_pexpect}
    rm -f %{buildroot}%{python2_sitearch}/pexpect
%endif

%if %{with sphinx_hack}
    rm -fr %{buildroot}%{python2_sitearch}/sphinx
%endif

# More wrong buildroot references
perl -pi -e 's|%{buildroot}||g;' \
	 -e "s|$PWD/src/doc|%{SAGE_DOC}|g;" \
    %{buildroot}%{SAGE_DOC}/output/html/en/reference/todolist.html
# with docs
%endif

# Script was used to build documentation
perl -pi -e 's|%{buildroot}||g;s|^##||g;' %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
# Fix links
rm -fr $SAGE_SRC/sage $SAGE_ETC/sage $SAGE_ROOT/doc $SAGE_SRC/doc
rm -fr $SAGE_ROOT/share $SAGE_ROOT/devel
ln -sf %{python2_sitearch}/sage $SAGE_SRC/sage
ln -sf %{python2_sitearch} $SAGE_ETC/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
ln -sf %{SAGE_DOC} $SAGE_SRC/doc
ln -sf %{SAGE_SHARE} $SAGE_ROOT/share
# compat devel symlink
ln -sf src $SAGE_ROOT/devel

# Install menu and icons
pushd build/pkgs/sagenb/src/sagenb/data
    install -p -m644 -D sage/images/icon128x128.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
popd
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Sagemath
Comment=A free open-source mathematics software system
Exec=sage
Icon=%{name}
Terminal=true
Type=Application
Categories=Science;Math;
EOF
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# Fix permissions
find %{buildroot} -name '*.so' | xargs chmod 755
pushd %{buildroot}%{SAGE_LOCAL}/bin
    chmod 755 QuadraticSieve
    chmod 755 mcube dikcube cu2 size222 cubex optimal
popd
for file in `find %{buildroot} -name \*.py`; do
    if head -1 $file | grep -q '^#!'; then
	chmod +x $file
    fi
done

%if %{with docs}
chmod -x %{buildroot}%{SAGE_DOC}/en/prep/media/Rplot001.png

# Documentation is not rebuilt (also corrects rpmlint warning of hidden file)
find %{buildroot}%{SAGE_DOC} -name .buildinfo -exec rm {} \;
rm -fr %{buildroot}%{SAGE_DOC}/output/inventory
find %{buildroot}%{SAGE_DOC} -type d -name _sources | xargs rm -fr
%endif

# remove .po files
rm %{buildroot}%{python2_sitearch}/sagenb/translations/*/LC_MESSAGES/*.po

%if %{without sage3d}
rm -r %{buildroot}%{python2_sitearch}/sagenb/data/sage3d
%endif

# remove build directory in buildroot
[ -d %{buildroot}%{SAGE_SRC}/build ] &&
    rm -r %{buildroot}%{SAGE_SRC}/build

%if %{with bundled_pari}
install -D -m 755 %{_builddir}/bin/gp-2.8 %{buildroot}%{SAGE_LOCAL}/bin/gp-2.8
for dest in gp sage_pari; do
    ln -sf gp-2.8 %{buildroot}%{SAGE_LOCAL}/bin/$dest
done
install -D -m 755 %{_builddir}/lib/libpari-gmp-2.8.so.0.0.0 \
    %{buildroot}%{SAGE_ROOT}/lib/libpari-gmp-2.8.so.0.0.0
ln -s libpari-gmp-2.8.so.0.0.0 \
    %{buildroot}%{SAGE_ROOT}/lib/libpari-gmp-2.8.so.0
install -D -m 644 %{_builddir}/share/pari/pari.desc \
    %{buildroot}%{SAGE_LOCAL}/pari.desc

# make sure pari is in link path
ln -s libpari-gmp-2.8.so.0.0.0 %{buildroot}%{SAGE_ROOT}/lib/libpari.so
perl -pi -e 's|(libdirs = cblas_library_dirs)|$1 + \["%{SAGE_ROOT}/lib"\]|;' %{buildroot}%{python2_sitearch}/sage/misc/cython.py
%endif

%if %{without install_hack}
# remove sage_setup
rm -r %{buildroot}%{python2_sitearch}/sage_setup
%endif

# pretend sagemath spkgs are installed to reduce number of errors
# in doctests
mkdir -p %{buildroot}%{SAGE_SPKG_INST}
pushd upstream
for file in *.tar.*; do
    touch %{buildroot}%{SAGE_SPKG_INST}/$(echo $file | sed -e 's|\.tar.*||')
done
popd
#------------------------------------------------------------------------
cat > %{buildroot}%{SAGE_LOCAL}/bin/sage-list-packages << EOF
#!/bin/sh
NOVERSION=false
INSTALLED=no
while [ \$# -gt 0 ]; do
    if [ x\$1 = x--no-version ]; then
	NOVERSION=true
    elif [ x\$1 = xinstalled ]; then
        INSTALLED=yes
    fi
    shift
done
if [ \$INSTALLED = no ]; then
    exit 0
fi
LIST=\$(cd %{SAGE_SPKG_INST}; echo *)
if [ \$NOVERSION = false ]; then
    for pkg in \$LIST; do
	echo \$pkg | sed -e 's/-/ /'
    done
else
    for pkg in \$LIST; do
	echo \$pkg | sed -e 's/-.*//'
    done
fi
EOF
chmod +x %{buildroot}%{SAGE_LOCAL}/bin/sage-list-packages
#------------------------------------------------------------------------

%if %{with docs}
    # do not install symlink to '.'
    rm %{buildroot}%{SAGE_DOC}/output
%endif

# last install command
rm -fr $DOT_SAGE

########################################################################
# Use symlinks and a minor patch to the notebook to not bundle jmol
%post		notebook
ln -sf %{_javadir}/JmolApplet.jar %{python2_sitearch}/sagenb/data/jmol/
ln -sf %{_javadir}/Jmol.jar %{python2_sitearch}/sagenb/data/jmol/
ln -sf %{_javadir}/vecmath.jar %{python2_sitearch}/sagenb/data/jmol/
exit 0

%postun		notebook
if [ $1 -eq 0 ] ; then
    rm -f %{python2_sitearch}/sagenb/data/jmol/JmolApplet.jar
    rm -f %{python2_sitearch}/sagenb/data/jmol/Jmol.jar
    rm -f %{python2_sitearch}/sagenb/data/jmol/vecmath.jar
    rmdir %{python2_sitearch}/sagenb/data/jmol &&
	rmdir %{python2_sitearch}/sagenb/data &&
	    rmdir %{python2_sitearch}/sagenb
fi
exit 0

%post		sagetex
%{_bindir}/mktexlsr
exit 0

%postun		sagetex
if [ $1 -eq 0 ] ; then
    %{_bindir}/mktexlsr
fi
exit 0

########################################################################
%files
# GPLv2+
%dir %{SAGE_ROOT}
%doc %{SAGE_ROOT}/COPYING.txt
%dir %{SAGE_LOCAL}
%dir %{SAGE_LOCAL}/bin
%{SAGE_LOCAL}/bin/QuadraticSieve
%{SAGE_LOCAL}/bin/ecm
%{SAGE_LOCAL}/bin/gap_stamp
%if %{with bundled_pari}
%{SAGE_LOCAL}/bin/gp*
%endif
%{SAGE_LOCAL}/bin/jmol
%if %{with bundled_ipython}
%{SAGE_LOCAL}/bin/ip*
%endif
%{SAGE_LOCAL}/bin/python
%{SAGE_LOCAL}/bin/sage*
%{SAGE_LOCAL}/include
%{SAGE_LOCAL}/lib
%{SAGE_LOCAL}/share
%{SAGE_ROOT}/doc
%{SAGE_ROOT}/devel
%{SAGE_ROOT}/share
%dir %{SAGE_SRC}
%if %{with docs}
%{SAGE_SRC}/doc
%endif
%{SAGE_SRC}/sage
%dir %{SAGE_PYTHONPATH}
# GPLv2+
%{_bindir}/sage
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%if %{with bundled_pari}
%{SAGE_ROOT}/lib
%{SAGE_LOCAL}/pari.desc
%endif

#------------------------------------------------------------------------
%files		core
# GPLv2+
%{SAGE_LOCAL}/bin/cysignals*
%{python2_sitearch}/sage
%if %{without install_hack}
%{python2_sitearch}/sage-*.egg-info
%endif
%{python2_sitearch}/cysignals
%{python2_sitearch}/cysignals-*.egg-info
%if %{with bundled_ipython}
%{SAGE_PYTHONPATH}/IPython
%endif
#------------------------------------------------------------------------
%files		data
%dir %{SAGE_SHARE}
%dir %{SAGE_ETC}
%{SAGE_ETC}/sage
%{SAGE_ETC}/gprc.expect

#------------------------------------------------------------------------
%files		data-conway_polynomials
# GPLv2+
%{SAGE_SHARE}/conway_polynomials

#------------------------------------------------------------------------
%files		data-elliptic_curves
# GPLv2+
%{SAGE_SHARE}/cremona
%{SAGE_SHARE}/ellcurves

#------------------------------------------------------------------------
%files		data-etc
# GPLv2+
%{SAGE_ETC}/gap
%{SAGE_ETC}/images
%{SAGE_ETC}/magma
%{SAGE_ETC}/mwrank
%{SAGE_ETC}/pari

#------------------------------------------------------------------------
%files		data-graphs
# GPLv2+
%{SAGE_ETC}/graphs
%{SAGE_SHARE}/graphs

#------------------------------------------------------------------------
%files		data-polytopes_db
# GPL+
%{SAGE_SHARE}/reflexive_polytopes

%if %{with docs}
#------------------------------------------------------------------------
%files		doc
# GPLv2+
%dir %{SAGE_DOC}
%{SAGE_DOC}/common
%dir %{SAGE_DOC}/output
%dir %{SAGE_DOC}/output/html

#------------------------------------------------------------------------
%files		doc-de
# GPLv2+
%{SAGE_DOC}/de
%{SAGE_DOC}/output/html/de

#------------------------------------------------------------------------
%files		doc-en
# GPLv2+
%{SAGE_DOC}/en
%{SAGE_DOC}/output/html/en

#------------------------------------------------------------------------
%files		doc-fr
# GPLv2+
%{SAGE_DOC}/fr
%{SAGE_DOC}/output/html/fr

#------------------------------------------------------------------------
%files		doc-pt
# GPLv2+
%{SAGE_DOC}/pt
%{SAGE_DOC}/output/html/pt

#------------------------------------------------------------------------
%files		doc-ru
# GPLv2+
%{SAGE_DOC}/ru
%{SAGE_DOC}/output/html/ru

#------------------------------------------------------------------------
%files		doc-tr
# GPLv2+
%{SAGE_DOC}/tr
%{SAGE_DOC}/output/html/tr

# with docs
%endif

#------------------------------------------------------------------------
%files		notebook
%{SAGE_ETC}/notebook-ipython
# GPLv2+
%{SAGE_SRC}/sagenb
%dir %{python2_sitearch}/sagenb
%{python2_sitearch}/sagenb/*.py*
%{python2_sitearch}/sagenb-*.egg-info
%dir %{python2_sitearch}/sagenb/data
# BSD
%{python2_sitearch}/sagenb/data/codemirror
# MIT
%{python2_sitearch}/sagenb/data/graph_editor
# ASL 2.0
%{python2_sitearch}/sagenb/data/highlight
# LGPLv2+
%{SAGE_SHARE}/jsmol
# (MIT or GPLv2) and (MIT and BSD and GPL)
%{python2_sitearch}/sagenb/data/jquery
# (MIT or GPLv2) and (MIT and BSD and GPL)
%{python2_sitearch}/sagenb/data/jqueryui
# Public Domain
%{python2_sitearch}/sagenb/data/json
# ASL 2.0
%{python2_sitearch}/sagenb/data/mathjax
# Empty (do not run doctests flag file)
%{python2_sitearch}/sagenb/data/nodoctest.py*
# BSD
%{python2_sitearch}/sagenb/data/openid-realselector
# GPLv2+
%{python2_sitearch}/sagenb/data/sage
%if %{with sage3d}
# GPLv2+
%{python2_sitearch}/sagenb/data/sage3d
%endif
# LGPLv2+
%{python2_sitearch}/sagenb/data/tiny_mce
# LGPLv2+
%{python2_sitearch}/sagenb/data/zorn
# GPLv2+
%{python2_sitearch}/sagenb/flask_version
# GPLv2+
%{python2_sitearch}/sagenb/interfaces
# GPLv2+
%{python2_sitearch}/sagenb/misc
# GPLv2+
%{python2_sitearch}/sagenb/notebook
# GPLv2+
%{python2_sitearch}/sagenb/simple
# GPLv2+
%{python2_sitearch}/sagenb/storage
# GPLv2+
%dir %{python2_sitearch}/sagenb/testing
%{python2_sitearch}/sagenb/testing/*.py*
%{python2_sitearch}/sagenb/testing/tests
# ASL 2.0
%{python2_sitearch}/sagenb/testing/selenium
# GPLv2+
%dir %{python2_sitearch}/sagenb/translations
%lang(cs_CZ) %{python2_sitearch}/sagenb/translations/cs_CZ
%lang(de_AT) %{python2_sitearch}/sagenb/translations/de_AT
%lang(de_AT) %{python2_sitearch}/sagenb/translations/en_US
%lang(de_AT) %{python2_sitearch}/sagenb/translations/es_ES
%lang(de_AT) %{python2_sitearch}/sagenb/translations/fr_FR
%lang(pt_BR) %{python2_sitearch}/sagenb/translations/pt_BR
%lang(ru_RU) %{python2_sitearch}/sagenb/translations/ru_RU
%lang(uk_UA) %{python2_sitearch}/sagenb/translations/uk_UA

#------------------------------------------------------------------------
%files		rubiks
# GPL+
%{SAGE_LOCAL}/bin/optimal
# MIT
%{SAGE_LOCAL}/bin/dikcube
%{SAGE_LOCAL}/bin/size222
# GPL+
%{SAGE_LOCAL}/bin/cu2
%{SAGE_LOCAL}/bin/cubex
%{SAGE_LOCAL}/bin/mcube

#------------------------------------------------------------------------
%files		sagetex
# GPLv2+
%{python2_sitearch}/sagetex*
%{_datadir}/texmf/tex/latex/sagetex
%doc %{_docdir}/sagetex
