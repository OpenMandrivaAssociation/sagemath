#%#define __noautoprov		'[^l][^i][^b]([-a-zA-Z_]+)\.so\(\)'

# not functional due to missing jar dependencies
%global with_sage3d		0

%global with_sphinx_hack	1

# sagemath works only with pexpect-2.0
%global with_sage_pexpect	1

%global have_lrcalc		1

%global have_coin_or_Cbc	0

%global have_libgap		0

%ifarch x86_64
%global have_fes		1
%else
%global have_fes		0
%endif

# set to run sage -testall in %%install
%global with_check		0
%global SAGE_TIMEOUT		60
%global SAGE_TIMEOUT_LONG	180

%global conway_polynomials_pkg	conway_polynomials-0.4.p0
%global	elliptic_curves_pkg	elliptic_curves-0.7
%global	flintqs_pkg		flintqs-20070817.p8
%global graphs_pkg		graphs-20120404.p4
%global pexpect_pkg		pexpect-2.0.p5
%global polytopes_db_pkg	polytopes_db-20120220
%global rubiks_pkg		rubiks-20070912.p18
%global	sagenb_pkg		sagenb-0.10.4
%global sagetex_pkg		sagetex-2.3.4

%global sagemath_share		%{_datadir}/%{name}

%global SAGE_ROOT		%{_libdir}/sagemath
%global SAGE_LOCAL		%{SAGE_ROOT}/local
%global SAGE_SRC		%{SAGE_ROOT}/src
%global SAGE_DOC		%{_docdir}/%{name}
%global SAGE_SHARE		%{_datadir}/sagemath
%global SAGE_EXTCODE		%{SAGE_SHARE}/ext
%global SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		sagemath
Group:		Sciences/Mathematics
Summary:	A free open-source mathematics software system
Version:	5.10
Release:	1%{?dist}
# The file ${SAGE_ROOT}/COPYING.txt is the upstream license breakdown file
# Additionally, every $files section has a comment with the license name
# before files with that license
License:	ASL 2.0 and BSD and GPL+ and GPLv2+ and LGPLv2+ and MIT and Public Domain
URL:		http://www.sagemath.org
Source0:	http://boxen.math.washington.edu/home/%{name}/sage-mirror/src/sage-%{version}.tar
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
Patch4:		%{name}-ntl6.patch

# remove call to not implemented sagemath "is_package_installed" interfaces
# need to package coin-or solver in fedora
# remove check for non free solvers
Patch5:		%{name}-extensions.patch

# helper to:
#	o respect a DESTDIR environment variable
#	o avoid double '//' in pathnames, what can confused debugedit & co
#	o minor change to help in incremental builds by avoiding rebuilding
#	  files
#	o do not assume there is an installed sagemath
Patch6:		%{name}-rpmbuild.patch

# build documentation in buildroot environment
Patch7:		%{name}-sagedoc.patch

# sage notebook rpm and system environment adjustments
Patch8:		%{name}-sagenb.patch

# do not attempt to create state files in system directories
Patch9:		%{name}-readonly.patch

# force coercion of ecl t_string to ecl t_base_string
# this is hackish and only required if ecl is built with unicode support
Patch10:		%{name}-ecl-unicode.patch

# do not link explicitly to png12
Patch11:	%{name}-png.patch

# work with all maxima-runtime lisp backend packages
Patch12:	%{name}-maxima.patch

# execute 4ti2 programs in $PATH not in $SAGE_ROOT/local/bin
Patch13:	%{name}-4ti2.patch

# http://trac.sagemath.org/sage_trac/ticket/12992
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1317
Patch14:	%{name}-pari.patch

# in fedora 18 it was updated to latest fplll
Patch15:	%{name}-fplll.patch

# Portuguese translations: http://trac.sagemath.org/sage_trac/ticket/12822
Patch16:	trac_12502_pt_translation_of_a_tour_of_sage_rebase1.patch
Patch17:	trac_12822_pt_translation_of_tutorial.patch
Patch18:	trac_12822_pt_translation_of_tutorial_rev1.patch

# use jmol itself to export preview images
# FIXME besides not using X and told so, fails if DISPLAY is not set
Patch20:	%{name}-jmol.patch

# adapt for maxima 5.29.1 package
Patch21:	%{name}-maxima.system.patch

# only cremona mini database built and installed
# FIXME add a package with the full cremona database
# FIXME actually it should be already available in pari-elldata
Patch22:	%{name}-cremona.patch

# lrslib is a requires
Patch23:	%{name}-lrslib.patch

# nauty cannot be packaged due to license restrictions
# http://cs.anu.edu.au/~bdm/nauty/
# http://pallini.di.uniroma1.it/
Patch24:	%{name}-nauty.patch

# gap hap package not (yet) available
# http://www-gap.mcs.st-and.ac.uk/Packages/hap.html
Patch25:	%{name}-gap-hap.patch

# Patch to enable lrcalc once review request is done in Fedora
Patch26:	%{name}-lrcalc.patch

# Patch to enable cbc once review requests are done in Fedora
Patch27:	%{name}-cbc.patch

# Patch to enable libgap once review request is done in Fedora
Patch28:	%{name}-libgap.patch

# Patch to disable libgap because it is not optional by default
Patch29:	%{name}-nolibgap.patch

# Patch to enable fes once review requests are done in Fedora
Patch30:	%{name}-fes.patch

# Get package to build with known problem if not yet updated to pari 2.6.
Patch31:	%{name}-nopari2.6.patch

# sagemath 5.8 (optionally) requires cryptominisat 2.9.6 (in rawhide)
# and does not work with cryptominisat 2.9.5 (in f18)
Patch32:	%{name}-cryptominisat.patch

# Adapt to m4rie 20130416
Patch33:	%{name}-m4rie.patch

# Until cython is fixed for f18 and f19; just override wrong cython definition
# https://bugzilla.redhat.com/show_bug.cgi?id=961372
Patch34:	%{name}-rh_bz_961372.patch

# Mandriva specific
Patch35:	%{name}-underlink.patch

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
%if %{have_libgap}
BuildRequires:	libgap-devel
%endif
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
Requires:	%{name}-data-conway_polynomials%{?_isa} = %{version}-%{release}
Requires:	%{name}-data-elliptic_curves%{?_isa} = %{version}-%{release}
Requires:	%{name}-data-extcode%{?_isa} = %{version}-%{release}
Requires:	%{name}-data-graphs%{?_isa} = %{version}-%{release}
Requires:	%{name}-data-polytopes_db%{?_isa} = %{version}-%{release}

%description	data
Collection of databases and interface customization scripts for sagemath.

#------------------------------------------------------------------------
%package	data-conway_polynomials
Summary:	Conway Polynomials Database
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	data-conway_polynomials
Small database of Conway polynomials for sagemath.

#------------------------------------------------------------------------
%package	data-elliptic_curves
Summary:	Databases of elliptic curves
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	data-elliptic_curves
Includes two databases:

 * A small subset of the data in John Cremona's database of elliptic curves up
   to conductor 10000. See http://www.warwick.ac.uk/~masgaj/ftp/data/ or
   http://sage.math.washington.edu/cremona/INDEX.html

 * William Stein's database of interesting curves

#------------------------------------------------------------------------
%package	data-extcode
Summary:	Extcode for Sagemath
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	data-extcode
Collection of scripts and interfaces to sagemath.

#------------------------------------------------------------------------
%package	data-graphs
Summary:	Sagemath database of graphs
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	data-graphs
A database of graphs. Created by Emily Kirkman based on the work of Jason
Grout. Since April 2012 it also contains the ISGCI graph database.

#------------------------------------------------------------------------
%package	data-polytopes_db
Summary:	Lists of 2- and 3-dimensional reflexive polytopes
Group:		Sciences/Mathematics
Requires:	%{name}%{?_isa} = %{version}-%{release}

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

%description	doc
This package contains the documentation infrastructure for %{name}.

#------------------------------------------------------------------------
%package	doc-de
Summary:	German documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

%description	doc-de
This package contains the German %{name} documentation.

#------------------------------------------------------------------------
%package	doc-en
Summary:	English documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

%description	doc-en
This package contains the English %{name} documentation.

#------------------------------------------------------------------------
%package	doc-fr
Summary:	French documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

%description	doc-fr
This package contains the French %{name} documentation.

#------------------------------------------------------------------------
%package	doc-pt
Summary:	Portuguese documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

%description	doc-pt
This package contains the Portuguese %{name} documentation.

#------------------------------------------------------------------------
%package	doc-ru
Summary:	Russian documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

%description	doc-ru
This package contains the Russian %{name} documentation.

#------------------------------------------------------------------------
%package	doc-tr
Summary:	Turkish documentation files for %{name}
Group:		Sciences/Mathematics
Requires:	%{name}-doc%{?_isa} = %{version}-%{release}

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
In summary the three contributers are:

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

mkdir -p spkg/build
pushd spkg/build
    for pkg in					\
	%{conway_polynomials_pkg}		\
	%{elliptic_curves_pkg}			\
	extcode-%{version}			\
	%{flintqs_pkg}				\
	%{graphs_pkg}				\
%if %{with_sage_pexpect}
	%{pexpect_pkg}				\
%endif
	%{polytopes_db_pkg}			\
	%{rubiks_pkg}				\
	%{sagenb_pkg}				\
	%{sagetex_pkg}				\
	sage-%{version}				\
	sage_scripts-%{version}			\
    ; do
	tar jxf ../standard/$pkg.spkg
    done

    # apply in spkgs that do not have patches already applied
    # or that actually have patches
pushd %{flintqs_pkg}/src
    for diff in `ls ../patches/*.patch`; do
	patch -p1 < $diff
    done
popd

pushd %{sagenb_pkg}/src
    tar zxf %{sagenb_pkg}.tar.gz
    mv  %{sagenb_pkg} sagenb
popd

%if %{with_sage_pexpect}
    pushd %{pexpect_pkg}/src
	for diff in `ls ../patches/*.patch ../patches/*.diff`; do
	    patch -p1 < $diff
	done
    popd
%endif
    pushd %{rubiks_pkg}
	cp patches/dietz-mcube-Makefile src/dietz/mcube/Makefile
	cp patches/dietz-solver-Makefile src/dietz/solver/Makefile
	cp patches/dietz-cu2-Makefile src/dietz/cu2/Makefile
	cp patches/reid-Makefile src/reid/Makefile
    popd
popd

%patch0 -p1
%patch1 -p1
%patch2 -p1

%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

pushd spkg/build/sage-%{version}
mkdir -p doc/pt/a_tour_of_sage/
cp -fa doc/en/a_tour_of_sage/*.png doc/pt/a_tour_of_sage/

%patch16 -p1
%patch17 -p1
%patch18 -p1
popd

%patch20 -p1

# Not required for Mandriva
%if 0
%patch21 -p1
%endif

%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1

%if %{have_lrcalc}
%patch26 -p1
%endif

# other coin-or packages are build requires or coin-or-Cbc
%if %{have_coin_or_Cbc}
%patch27 -p1
%endif

%if %{have_libgap}
%patch28 -p1
%else
%patch29 -p1
%endif

%if %{have_fes}
%patch30 -p1
%endif

%patch31 -p1
%patch32 -p1
# Not required for Mandriva
%if 0
%patch33 -p1
%endif
%patch34 -p1

%patch35 -p1

#------------------------------------------------------------------------
# ensure proper/preferred libatlas is in linker path
pushd spkg/build/sage-%{version}
    perl -pi -e 's|^(extra_link_args = ).*|$1\["-L%{_libdir}/atlas"\]|;' sage/misc/cython.py
    # some .c files are not (re)generated
    find . \( -name \*.pyx -o -name \*.pxd \) | xargs touch
popd

# remove bundled jar files before build
rm spkg/build/%{sagenb_pkg}/src/sagenb/sagenb/data/sage3d/lib/sage3d.jar

# remove binary egg
rm -r spkg/build/%{sagenb_pkg}/src/sagenb/sagenb.egg-info

########################################################################
%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_SRC=%{buildroot}%{SAGE_SRC}
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`
export DESTDIR=%{buildroot}
# Use file in /tmp because there are issues with long pathnames
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

# match system packages as sagemath packages
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_SRC=%{buildroot}%{SAGE_SRC}
mkdir -p $SAGE_ROOT $SAGE_LOCAL $SAGE_SRC
ln -sf $PWD/spkg/build/sage-%{version}/sage $SAGE_SRC/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    pushd c_lib
	# scons ignores most environment variables
	# and does not have soname support
	sed -e 's|@@includedir@@|%{_includedir}|g' \
	    -e 's|@@libdir@@|%{_libdir}|g' \
	    -e 's|@@optflags@@|%{optflags}|g' \
	    -e 's|@@ldflags@@|%{ldflags}|g' \
	    -i SConstruct
	CXX=g++ UNAME=Linux SAGE64=auto scons
	ln -s libcsage.so.0 libcsage.so
    popd
    pushd sage/libs/mpmath
	dos2unix ext_impl.pxd ext_libmp.pyx ext_main.pxd ext_main.pyx
    popd
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/%{sagenb_pkg}/src/sagenb
    python ./setup.py build
popd

#------------------------------------------------------------------------
pushd spkg/build/%{flintqs_pkg}/src
    make %{?_smpflags} CPP="g++ %{optflags} -fPIC"
popd

pushd spkg/build/%{rubiks_pkg}/src
    make %{?_smp_mflags} CC="gcc -fPIC" CXX="g++ -fPIC" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
popd

# last build command
rm -fr $DOT_SAGE

########################################################################
%install
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_SRC=%{buildroot}%{SAGE_SRC}
export SAGE_SHARE=%{buildroot}%{SAGE_SHARE}
export SAGE_EXTCODE=%{buildroot}%{SAGE_EXTCODE}
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
ln -sf $PWD/spkg/build/sage-%{version}/sage $SAGE_SRC/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so.0 %{buildroot}%{_libdir}
    ln -sf libcsage.so.0 %{buildroot}%{_libdir}/libcsage.so
    pushd sage
	# install sage notebook templates
	cp -fa server/notebook/templates %{buildroot}%{python_sitearch}/sage/server/notebook
    popd
    # install documentation sources
    rm -fr $SAGE_DOC/{common,en,fr}
    cp -far doc/{common,de,en,fr,pt,ru,tr} $SAGE_DOC
popd

#------------------------------------------------------------------------
pushd spkg/build/%{sagenb_pkg}/src/sagenb
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
%if %{with_sage_pexpect}
pushd spkg/build/%{pexpect_pkg}/src
    cp -f {ANSI,FSM,pexpect,pxssh,screen}.py $SAGE_PYTHONPATH
popd
%endif

#------------------------------------------------------------------------
cp -fa COPYING.txt $SAGE_ROOT
pushd spkg/build/sage_scripts-%{version}
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* $SAGE_LOCAL/bin
    pushd $SAGE_LOCAL/bin
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/gp sage_pari
	ln -sf %{_bindir}/gap gap_stamp
    popd
popd
install -p -m755 spkg/bin/sage $SAGE_LOCAL/bin

#------------------------------------------------------------------------
pushd spkg/build/%{flintqs_pkg}/src
    cp -fa QuadraticSieve $SAGE_LOCAL/bin
popd

pushd spkg/build/%{rubiks_pkg}/src
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
	sage-apply-ticket \
	sage-bdist \
	sage-build \
	sage-clone \
	sage-combinat \
	sage-crap \
	sage-list-experimental \
	sage-list-optional \
	sage-list-packages \
	sage-list-standard \
	sage-location \
	sage-make_devel_packages \
	sage-omega \
	sage-pkg \
	sage-pull \
	sage-push \
	sage-pypkg-location \
	sage-README-osx.txt \
	sage-rebaseall.bat \
	sage-rebaseall.sh \
	sage-rebase.bat \
	sage-rebase.sh \
	sage-rsyncdist \
	sage-sdist \
	sage-spkg-install \
	sage-startuptime.py \
	sage-sync-build.py \
	sage-test-import \
	sage-update \
	sage-update-build \
	sage-upgrade \
	spkg-install; do
	rm -f $file
    done
popd

#------------------------------------------------------------------------
pushd spkg/build/%{conway_polynomials_pkg}
    python ./spkg-install
popd

#------------------------------------------------------------------------
pushd spkg/build/%{elliptic_curves_pkg}
    python ./spkg-install
popd

#------------------------------------------------------------------------
pushd spkg/build/extcode-%{version}
    mkdir -p $SAGE_EXTCODE
    for dir in 			\
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
	octave			\
	QEPCAD			\
	scilab			\
	singular		\
	sobj; do
	COUNT=`find $dir -type f | wc -l `
	if [ $COUNT -gt 0 ]; then
	    cp -far $dir $SAGE_EXTCODE
	fi
	cp -far pari $SAGE_EXTCODE
    done
    cp -fa %{SOURCE1} $SAGE_EXTCODE/pari
popd

#------------------------------------------------------------------------
pushd spkg/build/%{graphs_pkg}
    mkdir -p $SAGE_SHARE/graphs
    cp -fa src/* $SAGE_SHARE/graphs
popd

#------------------------------------------------------------------------
pushd spkg/build/%{polytopes_db_pkg}
    mkdir -p $SAGE_SHARE/reflexive_polytopes
    cp -fa src/* $SAGE_SHARE/reflexive_polytopes
popd

#------------------------------------------------------------------------
pushd spkg/build/%{sagetex_pkg}/src
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
export DOT_SAGENB="\$DOT_SAGE"
mkdir -p \$DOT_SAGE/{maxima,sympow,tmp}
export SAGE_TESTDIR=\$DOT_SAGE/tmp
export SAGE_ROOT="$SAGE_ROOT"
export SAGE_LOCAL="$SAGE_LOCAL"
export SAGE_SHARE="$SAGE_SHARE"
export SAGE_EXTCODE="$SAGE_EXTCODE"
export SAGE_SRC="$SAGE_SRC"
##export SAGE_DOC="$SAGE_DOC"
export PATH=$SAGE_LOCAL/bin:%{_libdir}/4ti2/bin:\$PATH
export SINGULARPATH=%{_libdir}/Singular/LIB
export SINGULAR_BIN_DIR=%{_libdir}/Singular
##export PYTHONPATH="$SAGE_PYTHONPATH:\$SAGE_LOCAL/bin"
export SAGE_CBLAS=cblas
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=\`gfortran --print-file-name=libgfortran.so\`
export SYMPOW_DIR="\$DOT_SAGE/sympow"
export LC_MESSAGES=C
export LC_NUMERIC=C
export SAGE_BROWSER=firefox
MALLOC_CHECK_=1 $SAGE_LOCAL/bin/sage "\$@"
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
# o link with proper atlas
# o install csage headers
# o install .pxi and .pxd files
pushd spkg/build/sage-%{version}
    # make atlas/blas available to compiled sources
    perl -pi -e								\
	's|^(extra_link_args =).*|$1 ["-L%{_libdir}/atlas"]|;'		\
	%{buildroot}/%{python_sitearch}/sage/misc/cython.py
    # make csage headers available
    mkdir -p %{buildroot}/%{_includedir}/csage
    cp -fa c_lib/include/* %{buildroot}/%{_includedir}/csage
    for f in `find sage \( -name \*.pxi -o -name \*.pxd -o -name \*.pyx \)`; do
	install -p -D -m 0644 $f %{buildroot}/%{python_sitearch}/$f
    done
    # need this or will not "find" the files in the directory, and
    # fail to link with gmp
    touch %{buildroot}/%{python_sitearch}/sage/libs/gmp/__init__.py
popd

#------------------------------------------------------------------------
%if %{with_sage_pexpect}
    cp -f $SAGE_PYTHONPATH/{ANSI,FSM,pexpect,pxssh,screen}.py %{buildroot}%{python_sitearch}
%endif

# Build documentation, using %#{buildroot} environment
pushd spkg/build/sage-%{version}/doc
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
    sed -e 's|%{buildroot}||g' -i $SAGE_DOC/output/html/en/reference/sage/misc/hg.html
popd

%if %{with_check}
export SAGE_TIMEOUT=%{SAGE_TIMEOUT}
export SAGE_TIMEOUT_LONG=%{SAGE_TIMEOUT_LONG}
sage -testall --verbose || :
install -p -m644 $DOT_SAGE/tmp/test.log $SAGE_DOC/test.log
# remove buildroot references from test.log
sed -i 's|%{buildroot}||g' $SAGE_DOC/test.log
%endif

%if %{with_sage_pexpect}
    rm -f %{buildroot}%{python_sitearch}/{ANSI,FSM,pexpect,pxssh,screen}.py{,c}
%endif

%if %{with_sphinx_hack}
    rm -fr %{buildroot}%{python_sitearch}/sphinx
%endif

# Script was used to build documentation 
perl -pi -e 's|%{buildroot}||g;s|^##||g;' %{buildroot}%{_bindir}/sage

# More wrong buildroot references
perl -pi -e 's|%{buildroot}||g;' \
	 -e "s|$PWD/spkg/build/sage-%{version}/doc|%{SAGE_DOC}|g;" \
    %{buildroot}%{SAGE_DOC}/output/html/en/reference/todolist.html \
    %{buildroot}%{SAGE_DOC}/output/html/en/reference/misc/sage/misc/hg.html

#------------------------------------------------------------------------
# Fix links
rm -fr $SAGE_SRC/sage $SAGE_EXTCODE/sage $SAGE_ROOT/doc $SAGE_SRC/doc
rm -fr $SAGE_ROOT/share $SAGE_ROOT/devel
ln -sf %{python_sitearch}/sage $SAGE_SRC/sage
ln -sf %{python_sitearch} $SAGE_EXTCODE/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
ln -sf %{SAGE_DOC} $SAGE_SRC/doc
ln -sf %{SAGE_SHARE} $SAGE_ROOT/share
# compat devel symlink
ln -sf src $SAGE_ROOT/devel

# Install menu and icons
pushd spkg/build/extcode-%{version}
    install -p -m644 -D notebook/images/icon32x32.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
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

rm %{buildroot}%{python_sitearch}/sagenb/data/mathjax/.gitignore \
   %{buildroot}%{python_sitearch}/sagenb/data/mathjax/docs/.gitignore

# remove bundles fonts
rm -r %{buildroot}%{python_sitearch}/sagenb/data/mathjax/fonts

# remove .po files
rm %{buildroot}%{python_sitearch}/sagenb/translations/*/LC_MESSAGES/*.po

# remove zero length files
rm %{buildroot}%{python_sitearch}/sage/server/notebook/compress/all.py* \
   %{buildroot}%{python_sitearch}/sage/misc/test_cpickle_sage.py*

%if !%{with_sage3d}
rm -r %{buildroot}%{python_sitearch}/sagenb/data/sage3d
%endif

# last install command
rm -fr $DOT_SAGE

########################################################################
%pretrans
# Temporary due to moving directory to symlink
if [ ! -L %{SAGE_ROOT}/devel -a -d %{SAGE_ROOT}/devel ]; then
    mkdir %{SAGE_SRC}
    mv %{SAGE_ROOT}/devel/* %{SAGE_SRC}
    rmdir %{SAGE_ROOT}/devel
    ln -s src %{SAGE_ROOT}/devel
fi

# Use symlinks and a minor patch to the notebook to not bundle jmol
%post		notebook
ln -sf %{_javadir}/JmolApplet.jar %{python_sitearch}/sagenb/data/jmol/
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
%if %{with_sage_pexpect}
# MIT
%{SAGE_PYTHONPATH}/*.py*
%endif
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
%dir %{SAGE_EXTCODE}
%{SAGE_EXTCODE}/sage

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
%files		data-extcode
# GPLv2+
%{SAGE_EXTCODE}/gap
%{SAGE_EXTCODE}/images
%{SAGE_EXTCODE}/magma
%{SAGE_EXTCODE}/maxima
%{SAGE_EXTCODE}/mwrank
%{SAGE_EXTCODE}/pari
%{SAGE_EXTCODE}/singular

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
