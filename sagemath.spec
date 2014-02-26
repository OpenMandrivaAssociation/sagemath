#%#define __noautoprov		'[^l][^i][^b]([-a-zA-Z_]+)\.so\(\)'
%define __noautoreq		'pythonegg\(flask-oldsessions\).*'

# not functional due to missing jar dependencies
%global with_sage3d		0

%global with_sphinx_hack	1

%global have_lrcalc		1

%global have_coin_or_Cbc	0

%ifarch x86_64
%global have_fes		1
%else
%global have_fes		0
%endif

# set to run sage -testall in %%install
%global with_check		0
%global SAGE_TIMEOUT		60
%global SAGE_TIMEOUT_LONG	180

%global conway_polynomials_pkg	conway_polynomials-0.4
%global	elliptic_curves_pkg	elliptic_curves-0.7
%global	flintqs_pkg		flintqs-20070817
%global graphs_pkg		graphs-20120404
%global pexpect_pkg		pexpect-2.0
%global polytopes_db_pkg	polytopes_db-20120220
%global rubiks_pkg		rubiks-20070912
%global	sagenb_pkg		sagenb-0.10.8.2
%global sagetex_pkg		sagetex-2.3.4

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
Version:	6.1.1
Release:	7%{?dist}
# The file ${SAGE_ROOT}/COPYING.txt is the upstream license breakdown file
# Additionally, every $files section has a comment with the license name
# before files with that license
License:	ASL 2.0 and BSD and GPL+ and GPLv2+ and LGPLv2+ and MIT and Public Domain
URL:		http://www.sagemath.org
Source0:	http://boxen.math.washington.edu/home/%{name}/sage-mirror/src/sage-%{version}.tar.gz
Source1:	gprc.expect
Source2:	makecmds.sty
# not installed by jmol package, use one in sagemath jmol spkg
Source3:	Jmol.js
Source4:	JmolHelp.html
# from jmol-12.3.27.p2 spkg
Source5:	testjava.sh
Source6:	%{name}.rpmlintrc

# 1. scons ignores most environment variables
# 2. scons 2.2* does not have soname support (expected for scons 2.3*)
# This patch adds some regex substition templates for CFLAGS, etc, and
# minor adaptation from full scons patch at:
# http://scons.tigris.org/nonav/issues/showattachment.cgi/902/soname_func.py
# Discussed at:
# http://scons.tigris.org/issues/show_bug.cgi?id=2869
Patch0:		%{name}-scons.patch

# Upstream uses mpir not gmp, but the rpm package is tailored to use gmp
Patch1:		%{name}-gmp.patch

# Set of patches to work with system wide packages
Patch2:		%{name}-scripts.patch

# Adapt to ntl 6.0.0.
Patch3:		%{name}-ntl6.patch

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

# force coercion of ecl t_string to ecl t_base_string
# this is hackish and only required if ecl is built with unicode support
Patch9:		%{name}-ecl-unicode.patch

# do not link explicitly to png12
Patch10:	%{name}-png.patch

# work with all maxima-runtime lisp backend packages
Patch11:	%{name}-maxima.patch

# execute 4ti2 programs in $PATH not in $SAGE_ROOT/local/bin
Patch12:	%{name}-4ti2.patch

# http://trac.sagemath.org/sage_trac/ticket/12992
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1317
Patch13:	%{name}-pari.patch

# Portuguese translations: http://trac.sagemath.org/sage_trac/ticket/12822
Patch14:	trac_12502_pt_translation_of_a_tour_of_sage_rebase1.patch
Patch15:	trac_12822_pt_translation_of_tutorial.patch
Patch16:	trac_12822_pt_translation_of_tutorial_rev1.patch

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

# Patch to enable lrcalc once review request is done in Fedora
Patch22:	%{name}-lrcalc.patch

# Patch to enable cbc once review requests are done in Fedora
Patch23:	%{name}-cbc.patch

# Patch to enable libgap once review request is done in Fedora
Patch24:	%{name}-libgap.patch

# Patch to enable fes once review requests are done in Fedora
Patch25:	%{name}-fes.patch

# Get package to build with known problem if not yet updated to pari 2.6.
Patch26:	%{name}-nopari2.6.patch

# sagemath 5.8 (optionally) requires cryptominisat 2.9.6 (in rawhide)
# and does not work with cryptominisat 2.9.5 (in f18)
Patch27:	%{name}-cryptominisat.patch

# Side effect of using distro packages
# https://bugzilla.redhat.com/show_bug.cgi?id=974769
Patch28:	%{name}-sympy.patch

# Mandriva specific
Patch29:	%{name}-underlink.patch

BuildRequires:	4ti2
BuildRequires:	cddlib-devel
BuildRequires:	boost-devel
BuildRequires:	cliquer-devel
%if %{have_coin_or_Cbc}
BuildRequires:	coin-or-Cbc-devel
%endif
BuildRequires:	cryptominisat-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	ecl
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	factory-devel
%if %{have_fes}
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
BuildRequires:	ipython
BuildRequires:	lcalc-devel
BuildRequires:	libatlas-devel
BuildRequires:	libfac-devel
BuildRequires:	libgap-devel
BuildRequires:	libmpc-devel
BuildRequires:	libpari-devel
BuildRequires:	linalg-linbox-devel
%if %{have_lrcalc}
BuildRequires:	lrcalc-devel
%endif
BuildRequires:	m4ri-devel
BuildRequires:	m4rie-devel
# try to ensure a sane /dev will exist when building documentation
BuildRequires:	makedev
BuildRequires:	maxima-runtime-ecl
BuildRequires:	mpfi-devel
BuildRequires:	ntl-devel
BuildRequires:	polybori-devel
BuildRequires:	ppl-devel
BuildRequires:	pynac-devel
BuildRequires:	python-cython
BuildRequires:	python-devel
BuildRequires:	python-flask-autoindex
BuildRequires:	python-flask-babel
BuildRequires:	python-flask-openid
BuildRequires:	python-flask-silk
BuildRequires:	python-matplotlib
BuildRequires:	python-networkx
BuildRequires:	python-numpy-devel
BuildRequires:	python-scipy
BuildRequires:	python-twisted
BuildRequires:	python-twisted-web
BuildRequires:	python-twisted-web2
BuildRequires:	R
BuildRequires:	ratpoints-devel
BuildRequires:	readline-devel
BuildRequires:	rpy
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
Requires:	genus2reduction
Requires:	gfan
Requires:	gp2c
Requires:	iml-devel
Requires:	ipython
Requires:	java-plugin
Requires:	jmol
Requires:	jsmath-fonts
Requires:	libpari-devel
Requires:	lrslib
Requires:	maxima-gui
Requires:	maxima-runtime-ecl
Requires:	palp
Requires:	pari
Requires:	pari-data
Requires:	python-pycrypto
Requires:	python-cvxopt
BuildRequires:	python-cython
Requires:	python-flask-autoindex
Requires:	python-flask-babel
Requires:	python-flask-openid
Requires:	python-flask-silk
Requires:	python-matplotlib
Requires:	python-networkx
Requires:	python-parsing
Requires:	python-scipy
Requires:	python-sympy
Requires:	python-twisted-web
Requires:	python-twisted-web2
Requires:	R
Requires:	%{name}-core
Requires:	%{name}-data
Requires:	%{name}-doc-en
Requires:	%{name}-notebook
Requires:	%{name}-rubiks
Requires:	%{name}-sagetex
Requires:	singular
Requires:	sympow
Requires:	tachyon
Requires:	texlive
Requires:	vecmath

# Missing build requires on armv7hl
ExclusiveArch:	%{ix86} x86_64

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
%package	devel
Summary:	Development files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains the header files and development documentation
for %{name}.

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

pushd build/pkgs/pexpect
    tar jxf ../../../upstream/%{pexpect_pkg}.tar.bz2
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
    pushd src
	cp ../patches/dietz-mcube-Makefile dietz/mcube/Makefile
	cp ../patches/dietz-solver-Makefile dietz/solver/Makefile
	cp ../patches/dietz-cu2-Makefile dietz/cu2/Makefile
	cp ../patches/reid-Makefile reid/Makefile
    popd
popd

pushd build/pkgs/sagenb
    tar xf ../../../upstream/%{sagenb_pkg}.tar
    mv %{sagenb_pkg} src
    pushd src
	tar zxf %{sagenb_pkg}.tar.gz
    popd
popd

pushd build/pkgs/sagetex
    tar jxf ../../../upstream/%{sagetex_pkg}.tar.bz2
    mv %{sagetex_pkg} src
popd

%patch0
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8
%patch9
%patch10
%patch11
%patch12
%patch13

pushd src
mkdir -p doc/pt/a_tour_of_sage/
cp -fa doc/en/a_tour_of_sage/*.png doc/pt/a_tour_of_sage/
%patch14 -p1
%patch15 -p1
%patch16 -p1
popd

%patch17
%patch18
%patch19

%patch20
%patch21

%if %{have_lrcalc}
%patch22
%endif

# other coin-or packages are build requires or coin-or-Cbc
%if %{have_coin_or_Cbc}
%patch23
%endif

%patch24

%if %{have_fes}
%patch25
%endif

%patch26
%patch27
%patch28
%patch29

sed -e 's|@@SAGE_ROOT@@|%{SAGE_ROOT}|' \
    -e 's|@@SAGE_DOC@@|%{SAGE_DOC}|' \
    -i src/sage/env.py

sed -e "s|, 'flask-oldsessions>=0.10'||" \
    -e "s|'http://github.com/mitsuhiko/flask-oldsessions/tarball/master#egg=flask-oldsessions-0.10'||" \
    -i build/pkgs/sagenb/src/%{sagenb_pkg}/setup.py

#------------------------------------------------------------------------
# ensure proper/preferred libatlas is in linker path
perl -pi -e 's|^(extra_link_args = ).*|$1\["-L%{_libdir}/atlas"\]|;' src/sage/misc/cython.py
%if 0%{?fedora} > 20
perl -pi -e "s|return 'atlas'|return 'satlas'|;" src/sage/misc/cython.py
%endif
# some .c files are not (re)generated
find src/sage \( -name \*.pyx -o -name \*.pxd \) | xargs touch

# remove bundled jar files before build
rm build/pkgs/sagenb/src/%{sagenb_pkg}/sagenb/data/sage3d/lib/sage3d.jar

# remove binary egg
rm -r build/pkgs/sagenb/src/%{sagenb_pkg}/sagenb.egg-info

########################################################################
%build
export CC=%{__cc}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
# Avoid buildroot in gcc command line (use _builddir instead)
export SAGE_SRC="$PWD/src"
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`
export DESTDIR=%{buildroot}
# Use file in /tmp because there are issues with long pathnames
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

# match system packages as sagemath packages
mkdir -p $SAGE_ROOT $SAGE_LOCAL
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
pushd src/c_lib
    # scons ignores most environment variables
    # and does not have soname support
    sed -e 's|@@includedir@@|%{_includedir}|g' \
	-e 's|@@libdir@@|%{_libdir}|g' \
	-e 's|@@optflags@@|%{optflags}|g' \
	-e 's|@@__global_ldflags@@|%{ldflags}|g' \
	-i SConstruct
    CXX=g++ UNAME=Linux SAGE64=auto scons
    ln -s libcsage.so.0 libcsage.so
popd
pushd src/sage/libs/mpmath
    dos2unix ext_impl.pxd ext_libmp.pyx ext_main.pxd ext_main.pyx
popd
pushd src
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd build/pkgs/sagenb/src/%{sagenb_pkg}
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd build/pkgs/flintqs/src
    make %{?_smpflags} CPP="g++ %{optflags} -fPIC"
popd

pushd build/pkgs/rubiks/src
    make %{?_smp_mflags} CC="gcc -fPIC" CXX="g++ -fPIC" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
popd

# last build command
rm -fr $DOT_SAGE

########################################################################
%install
export CC=%{__cc}
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_SRC=%{buildroot}%{SAGE_SRC}
export SAGE_SHARE=%{buildroot}%{SAGE_SHARE}
export SAGE_ETC=%{buildroot}%{SAGE_ETC}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}
export SAGE_PYTHONPATH=%{buildroot}%{SAGE_PYTHONPATH}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH
export DESTDIR=%{buildroot}
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p $SAGE_PYTHONPATH
rm -fr $SAGE_LOCAL/{include,lib,share,notebook}
mkdir -p $SAGE_SHARE $SAGE_DOC $SAGE_LOCAL/bin $SAGE_SRC
ln -sf $PWD/src/sage $SAGE_SRC/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
pushd src
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so.0 %{buildroot}%{_libdir}
    ln -sf libcsage.so.0 %{buildroot}%{_libdir}/libcsage.so
    # install documentation sources
    rm -fr $SAGE_DOC/{common,en,fr}
    cp -far doc/{common,de,en,fr,pt,ru,tr} $SAGE_DOC
popd

#------------------------------------------------------------------------
pushd build/pkgs/sagenb/src/%{sagenb_pkg}
    rm -f %{buildroot}%{python_sitearch}/sagenb/data/sage3d/sage3d
    python setup.py install --root=%{buildroot} --install-purelib=%{python_sitearch}
    install -p -m0755 %{SOURCE5} $SAGE_LOCAL/bin/testjava.sh
    # jmol
    rm -fr %{buildroot}%{python_sitearch}/sagenb/data/jmol
    mkdir -p %{buildroot}%{python_sitearch}/sagenb/data/jmol/appletweb
    pushd %{buildroot}%{python_sitearch}/sagenb/data/jmol
	cp -fa %{SOURCE3} %{SOURCE4} appletweb
    popd
    # sage3d
    rm -f %{buildroot}%{_bindir}/sage3d
%if %{with_sage3d}
    ln -sf %{SAGE_LOCAL}/bin/sage3d %{buildroot}%{python_sitearch}/sagenb/data/sage3d/sage3d
%endif
    # flask stuff not installed
    cp -ar flask_version %{buildroot}%{python_sitearch}/sagenb
    ln -sf %{python_sitearch}/sagenb %{buildroot}%{SAGE_SRC}/sagenb
popd

#------------------------------------------------------------------------
pushd build/pkgs/pexpect/src
    cp -fa {ANSI,FSM,pexpect,pxssh,screen}.py $SAGE_PYTHONPATH
popd

#------------------------------------------------------------------------
cp -fa COPYING.txt $SAGE_ROOT
pushd src/bin
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* $SAGE_LOCAL/bin
    pushd $SAGE_LOCAL/bin
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/gp sage_pari
	ln -sf %{_bindir}/gap gap_stamp
    popd
popd
install -p -m755 src/bin/sage $SAGE_LOCAL/bin

#------------------------------------------------------------------------
pushd build/pkgs/flintqs/src
    cp -fa QuadraticSieve $SAGE_LOCAL/bin
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
    python ./spkg-install
popd

#------------------------------------------------------------------------
pushd build/pkgs/elliptic_curves
    python ./spkg-install
popd

#------------------------------------------------------------------------
pushd src/ext
    mkdir -p $SAGE_ETC
    for dir in 			\
	gap			\
	images			\
	magma			\
	maxima			\
	mwrank			\
	singular		\
	sobj; do
	COUNT=`find $dir -type f | wc -l `
	if [ $COUNT -gt 0 ]; then
	    cp -far $dir $SAGE_ETC
	fi
	cp -far pari $SAGE_ETC
    done
    cp -fa %{SOURCE1} $SAGE_ETC
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
    python setup.py install --root=%{buildroot} --install-purelib=%{python_sitearch}
    install -p -m 0644 -D %{SOURCE2} \
	%{buildroot}%{_datadir}/texmf/tex/generic/sagetex/makecmds.sty
    mv %{buildroot}%{_docdir}/{sagetex,%{sagetex_pkg}}
    mv %{buildroot}%{_datadir}/texmf/tex/generic/sagetex/CONTRIBUTORS \
	 %{buildroot}%{_docdir}/%{sagetex_pkg}
    for file in PKG-INFO README; do
	install -p -m 0644 $file %{buildroot}%{_docdir}/%{sagetex_pkg}/$file
    done
popd

#------------------------------------------------------------------------
cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export CUR=\`pwd\`
##export DOT_SAGE="\$HOME/.sage"
mkdir -p \$DOT_SAGE/{maxima,sympow,tmp}
export SAGE_TESTDIR=\$DOT_SAGE/tmp
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_SHARE="$SAGE_SHARE"
export SAGE_ETC="$SAGE_ETC"
export SAGE_SRC="$SAGE_SRC"
##export SAGE_DOC="$SAGE_DOC"
export PATH=$SAGE_LOCAL/bin:%{_libdir}/4ti2/bin:\$PATH
export SINGULARPATH=%{_libdir}/Singular/LIB
export SINGULAR_BIN_DIR=%{_libdir}/Singular
##export PYTHONPATH="$SAGE_PYTHONPATH:\$SAGE_LOCAL/bin"
%if 0%{?fedora}
export SAGE_CBLAS=blas
%else
export SAGE_CBLAS=cblas
%endif
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=\`gfortran --print-file-name=libgfortran.so\`
export SYMPOW_DIR="\$DOT_SAGE/sympow"
export LC_MESSAGES=C
export LC_NUMERIC=C
$SAGE_LOCAL/bin/sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
%if %{with_sage3d}
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
    # make csage headers available
    mkdir -p %{buildroot}%{_includedir}/csage
    cp -fa c_lib/include/* %{buildroot}%{_includedir}/csage
    for f in `find sage \( -name \*.pxi -o -name \*.pxd -o -name \*.pyx \)`; do
	install -p -D -m 0644 $f %{buildroot}%{python_sitearch}/$f
    done
    # need this or will not "find" the files in the directory, and
    # fail to link with gmp
    touch %{buildroot}%{python_sitearch}/sage/libs/gmp/__init__.py
popd

#------------------------------------------------------------------------
    cp -f $SAGE_PYTHONPATH/{ANSI,FSM,pexpect,pxssh,screen}.py %{buildroot}%{python_sitearch}

# Build documentation, using %#{buildroot} environment
pushd src/doc
    export SAGE_DOC=`pwd`
    export PATH=%{buildroot}%{_bindir}:$SAGE_LOCAL/bin:$PATH
    export SINGULARPATH=%{_libdir}/Singular/LIB
    export SINGULAR_BIN_DIR=%{_libdir}/Singular
    export LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{_libdir}/atlas:$LD_LIBRARY_PATH
    export PYTHONPATH=%{buildroot}%{python_sitearch}:$SAGE_PYTHONPATH:$SAGE_DOC

%if %{with_sphinx_hack}
    cp -far %{python_sitelib}/sphinx %{buildroot}%{python_sitearch}
    sed -i "s|\(source.startswith('>>>')\)|\1 or source.startswith('sage: ')|" \
	%{buildroot}%{python_sitearch}/sphinx/highlighting.py
%endif

    # there we go
    ln -sf %{buildroot}%{SAGE_DOC} $SAGE_SRC/doc
    python common/builder.py all html
    export SAGE_DOC=%{buildroot}%{SAGE_DOC}
    cp -far output $SAGE_DOC

    # should not be required and encodes buildroot
    rm -fr $SAGE_DOC/output/doctrees
popd

%if %{with_check}
export SAGE_TIMEOUT=%{SAGE_TIMEOUT}
export SAGE_TIMEOUT_LONG=%{SAGE_TIMEOUT_LONG}
sage -testall --verbose || :
install -p -m644 $DOT_SAGE/tmp/test.log $SAGE_DOC/test.log
# remove buildroot references from test.log
sed -i 's|%{buildroot}||g' $SAGE_DOC/test.log
%endif

    rm -f %{buildroot}%{python_sitearch}/{ANSI,FSM,pexpect,pxssh,screen}.py{,c}

%if %{with_sphinx_hack}
    rm -fr %{buildroot}%{python_sitearch}/sphinx
%endif

# Script was used to build documentation 
perl -pi -e 's|%{buildroot}||g;s|^##||g;' %{buildroot}%{_bindir}/sage

# More wrong buildroot references
perl -pi -e 's|%{buildroot}||g;' \
	 -e "s|$PWD/src/doc|%{SAGE_DOC}|g;" \
    %{buildroot}%{SAGE_DOC}/output/html/en/reference/todolist.html

#------------------------------------------------------------------------
# Fix links
rm -fr $SAGE_SRC/sage $SAGE_ETC/sage $SAGE_ROOT/doc $SAGE_SRC/doc
rm -fr $SAGE_ROOT/share $SAGE_ROOT/devel
ln -sf %{python_sitearch}/sage $SAGE_SRC/sage
ln -sf %{python_sitearch} $SAGE_ETC/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
ln -sf %{SAGE_DOC} $SAGE_SRC/doc
ln -sf %{SAGE_SHARE} $SAGE_ROOT/share
# compat devel symlink
ln -sf src $SAGE_ROOT/devel

# Install menu and icons
pushd build/pkgs/sagenb/src/%{sagenb_pkg}/sagenb/data
    install -p -m644 -D sage/images/icon32x32.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
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
chmod -x %{buildroot}%{SAGE_DOC}/en/prep/media/Rplot001.png

# Documentation is not rebuilt (also corrects rpmlint warning of hidden file)
find %{buildroot}%{SAGE_DOC} -name .buildinfo -exec rm {} \;
rm -fr %{buildroot}%{SAGE_DOC}/output/inventory
find %{buildroot}%{SAGE_DOC} -type d -name _sources | xargs rm -fr

# remove bundles fonts
rm -r %{buildroot}%{python_sitearch}/sagenb/data/mathjax/fonts

# remove .po files
rm %{buildroot}%{python_sitearch}/sagenb/translations/*/LC_MESSAGES/*.po

%if !%{with_sage3d}
rm -r %{buildroot}%{python_sitearch}/sagenb/data/sage3d
%endif

# remove cache files
rm -r %{buildroot}%{python_sitearch}/sagenb/data/.webassets-cache

# last install command
rm -fr $DOT_SAGE

########################################################################
# Use symlinks and a minor patch to the notebook to not bundle jmol
%post		notebook
ln -sf %{_javadir}/JmolApplet.jar %{python_sitearch}/sagenb/data/jmol/
ln -sf %{_javadir}/Jmol.jar %{python_sitearch}/sagenb/data/jmol/
ln -sf %{_javadir}/vecmath.jar %{python_sitearch}/sagenb/data/jmol/
exit 0

%postun		notebook
if [ $1 -eq 0 ] ; then
    rm -f %{python_sitearch}/sagenb/data/jmol/JmolApplet.jar
    rm -f %{python_sitearch}/sagenb/data/jmol/vecmath.jar
    rmdir %{python_sitearch}/sagenb/data/jmol &&
	rmdir %{python_sitearch}/sagenb/data &&
	    rmdir %{python_sitearch}/sagenb
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
%{SAGE_LOCAL}/bin/gap_stamp
%{SAGE_LOCAL}/bin/sage*
%{SAGE_LOCAL}/bin/testjava.sh
%{SAGE_LOCAL}/include
%{SAGE_LOCAL}/lib
%{SAGE_LOCAL}/share
%{SAGE_ROOT}/doc
%{SAGE_ROOT}/devel
%{SAGE_ROOT}/share
%dir %{SAGE_SRC}
%{SAGE_SRC}/doc
%{SAGE_SRC}/sage
%dir %{SAGE_PYTHONPATH}
# MIT
%{SAGE_PYTHONPATH}/*.py*
# GPLv2+
%{_bindir}/sage
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

#------------------------------------------------------------------------
%files		core
# GPLv2+
%{_libdir}/libcsage.so.*
%{python_sitearch}/sage
%{python_sitearch}/sage-*.egg-info

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
%{SAGE_ETC}/maxima
%{SAGE_ETC}/mwrank
%{SAGE_ETC}/pari
%{SAGE_ETC}/singular

#------------------------------------------------------------------------
%files		data-graphs
# GPLv2+
%{SAGE_SHARE}/graphs

#------------------------------------------------------------------------
%files		data-polytopes_db
# GPL+
%{SAGE_SHARE}/reflexive_polytopes

#------------------------------------------------------------------------
%files		devel
# GPLv2+
%{_includedir}/csage
%{_libdir}/libcsage.so

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

#------------------------------------------------------------------------
%files		notebook
# GPLv2+
%{SAGE_SRC}/sagenb
%dir %{python_sitearch}/sagenb
%{python_sitearch}/sagenb/*.py*
%{python_sitearch}/sagenb-*.egg-info
%dir %{python_sitearch}/sagenb/data
# BSD
%{python_sitearch}/sagenb/data/codemirror
# MIT
%{python_sitearch}/sagenb/data/graph_editor
# ASL 2.0
%{python_sitearch}/sagenb/data/highlight
# LGPLv2+
%{python_sitearch}/sagenb/data/jmol
# (MIT or GPLv2) and (MIT and BSD and GPL)
%{python_sitearch}/sagenb/data/jquery
# (MIT or GPLv2) and (MIT and BSD and GPL)
%{python_sitearch}/sagenb/data/jqueryui
# Public Domain
%{python_sitearch}/sagenb/data/json
# ASL 2.0
%{python_sitearch}/sagenb/data/mathjax
# Empty (do not run doctests flag file)
%{python_sitearch}/sagenb/data/nodoctest.py*
# BSD
%{python_sitearch}/sagenb/data/openid-realselector
# GPLv2+
%{python_sitearch}/sagenb/data/sage
%if %{with_sage3d}
# GPLv2+
%{python_sitearch}/sagenb/data/sage3d
%endif
# LGPLv2+
%{python_sitearch}/sagenb/data/tiny_mce
# Auto generated files
%{python_sitearch}/sagenb/data/webassets_generated
# LGPLv2+
%{python_sitearch}/sagenb/data/zorn
# GPLv2+
%{python_sitearch}/sagenb/flask_version
# GPLv2+
%{python_sitearch}/sagenb/interfaces
# GPLv2+
%{python_sitearch}/sagenb/misc
# GPLv2+
%{python_sitearch}/sagenb/notebook
# GPLv2+
%{python_sitearch}/sagenb/simple
# GPLv2+
%{python_sitearch}/sagenb/storage
# GPLv2+
%dir %{python_sitearch}/sagenb/testing
%{python_sitearch}/sagenb/testing/*.py*
%{python_sitearch}/sagenb/testing/tests
# ASL 2.0
%{python_sitearch}/sagenb/testing/selenium
# GPLv2+
%dir %{python_sitearch}/sagenb/translations
%lang(cs_CZ) %{python_sitearch}/sagenb/translations/cs_CZ
%lang(de_AT) %{python_sitearch}/sagenb/translations/de_AT
%lang(pt_BR) %{python_sitearch}/sagenb/translations/pt_BR
%lang(ru_RU) %{python_sitearch}/sagenb/translations/ru_RU

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
%{python_sitearch}/sagetex*
%{_datadir}/texmf/tex/generic/sagetex
%doc %{_docdir}/%{sagetex_pkg}
