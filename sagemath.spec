%global workaround_same_build_ID_in_nonidentical_files	1
%global _use_internal_dependency_generator	0
%global _exclude_files_from_autoprov		.*/site-packages/.*\.so

%global with_sphinx_hack	1

# may be required if not matching system version or to be updates proof
%global with_sage_cython	0

# ipython-0.11 drastically changed api since ipython-0.10.2
%global with_sage_ipython	1

# sagemath uses a somewhat old and heavily patched networkx
%global with_sage_networkx	0

# sagemath works only with pexpect-2.0
%global with_sage_pexpect	1

# set to run sage -testall in %%install
%global with_check		0
%global SAGE_TIMEOUT		60
%global SAGE_TIMEOUT_LONG	180

%global conway_polynomials_pkg	conway_polynomials-0.3
%global cython_pkg		cython-0.17pre
%global	elliptic_curves_pkg	elliptic_curves-0.7
%global	flintqs_pkg		flintqs-20070817.p8
%global graphs_pkg		graphs-20120404.p4
%global ipython_pkg		ipython-0.10.2.p1
%global networkx_pkg		networkx-1.6
%global pexpect_pkg		pexpect-2.0.p5
%global polytopes_db_pkg	polytopes_db-20100210.p2
%global rubiks_pkg		rubiks-20070912.p18
%global	sagenb_pkg		sagenb-0.10.2
%global sagetex_pkg		sagetex-2.3.3.p2

%global SAGE_ROOT		%{_libdir}/sagemath
%global SAGE_LOCAL		%{SAGE_ROOT}/local
%global SAGE_DEVEL		%{SAGE_ROOT}/devel
%global SAGE_DOC		%{SAGE_DEVEL}/doc
%global SAGE_SHARE		%{SAGE_ROOT}/share
%global SAGE_EXTCODE		%{SAGE_SHARE}/extcode
%global SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		sagemath
Group:		Sciences/Mathematics
Summary:	A free open-source mathematics software system
Version:	5.6
Release:	1%{?dist}
License:	BSD and GPLv2+ and LGPLv2+ and MIT
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

Patch0:		%{name}-gmp.patch
Patch1:		%{name}-scripts.patch
Patch2:		%{name}-unpatched_ntl.patch

# remove call to not implemented sagemath "is_package_installed" interfaces
# mpc is available in all modern linux distros
# need to package coin-or solver in fedora
# remove check for non free solvers
Patch3:		%{name}-extensions.patch

# helper to:
#	o respect a DESTDIR environment variable
#	o avoid double '//' in pathnames, what can confused debugedit & co
#	o minor change to help in incremental builds by avoiding rebuilding
#	  files
#	o do not assume there is an installed sagemath
Patch4:		%{name}-rpmbuild.patch

# avoid buildroot in some binaries due to not expanding symlinks
Patch5:		%{name}-buildroot.patch

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

# in rawhide it was updated to latest fplll
Patch14:	%{name}-fplll.patch

# Portuguese translations: http://trac.sagemath.org/sage_trac/ticket/12822
Patch15:	trac_12502_pt_translation_of_a_tour_of_sage_rebase1.patch
Patch16:	trac_12822_pt_translation_of_tutorial.patch
Patch17:	trac_12822_pt_translation_of_tutorial_rev1.patch

# wrappers for distros with libmpc 0.9
Patch18:	%{name}-libmpc.patch

# use jmol itself to export preview images
# FIXME besides not using X and told so, fails if DISPLAY is not set
Patch19:	%{name}-jmol.patch

# adapt for maxima 5.29.1 package
Patch20:	%{name}-maxima.system.patch

# only cremona mini database built and installed
# FIXME add a package with the full cremona database
# FIXME actually it should be already available in pari-elldata
Patch21:	%{name}-cremona.patch

# lrslib is a requires
Patch22:	%{name}-lrslib.patch

# nauty cannot be packaged due to license restrictions
# http://cs.anu.edu.au/~bdm/nauty/
# http://pallini.di.uniroma1.it/
Patch23:	%{name}-nauty.patch

# gap hap package not (yet) available
# http://www-gap.mcs.st-and.ac.uk/Packages/hap.html
Patch24:	%{name}-gap-hap.patch

# for buildsystems without /dev/shm available
Patch25:	%{name}-parallel.patch

BuildRequires:	4ti2
BuildRequires:	cddlib-devel
BuildRequires:	boost-devel
BuildRequires:	cliquer-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	ecl
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	factory-devel
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
BuildRequires:	lcalc-devel
BuildRequires:	libatlas-devel
BuildRequires:	libmpc-devel
BuildRequires:	libpari-devel
BuildRequires:	linalg-linbox-devel
BuildRequires:	m4ri-devel
BuildRequires:	m4rie-devel
# try to ensure a sane /dev will exist when building documentation
BuildRequires:	makedev
BuildRequires:	maxima-runtime-ecl
BuildRequires:	mpfi-devel
BuildRequires:	ntl-devel
BuildRequires:	polybori
BuildRequires:	ppl-devel
BuildRequires:	pynac-devel
BuildRequires:	python-devel
BuildRequires:	python-flask-autoindex
BuildRequires:	python-flask-babel
BuildRequires:	python-flask-openid
BuildRequires:	python-flask-silk
BuildRequires:	python-matplotlib
%if !%{with_sage_networkx}
BuildRequires:	python-networkx
%endif
BuildRequires:	python-numpy-devel
BuildRequires:	python-scipy
BuildRequires:	python-twisted
BuildRequires:	polybori-devel
BuildRequires:	ratpoints
BuildRequires:	readline-devel
BuildRequires:	scons
BuildRequires:	singular
BuildRequires:	singular-devel
BuildRequires:	symmetrica-devel

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
%if !%{with_sage_cython}
BuildRequires:	python-cython
%endif
Requires:	python-flask-autoindex
Requires:	python-flask-babel
Requires:	python-flask-openid
Requires:	python-flask-silk
Requires:	python-matplotlib
%if !%{with_sage_networkx}
Requires:	python-networkx
%endif
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
%if %{with_sage_cython}
	%{cython_pkg}				\
%endif
	%{elliptic_curves_pkg}			\
	extcode-%{version}			\
	%{flintqs_pkg}				\
	%{graphs_pkg}				\
%if %{with_sage_ipython}
	%{ipython_pkg}				\
%endif
%if %{with_sage_networkx}
	%{networkx_pkg}				\
%endif
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

%if %{with_sage_ipython}
    pushd %{ipython_pkg}/src
	for diff in `ls ../patches/*.patch ../patches/*.diff`; do
	    patch -p1 < $diff
	done
    popd
%endif
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
# patch2 is only for fedora or if droping NTL sagemath patch
%patch3 -p1
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

pushd spkg/build/sage-%{version}
mkdir -p doc/pt/a_tour_of_sage/
cp -fa doc/en/a_tour_of_sage/*.png doc/pt/a_tour_of_sage/
%patch15 -p1
%patch16 -p1
%patch17 -p1
popd

#%#patch18 -p1		# if pre libmpc1
%patch19 -p1

%if 0%{?fedora} >= 18
%patch20 -p1
%endif

%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

%patch25 -p1

# make sure buildroot is clean
rm -rf %{buildroot}

# match system packages as sagemath packages
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
mkdir -p $SAGE_ROOT $SAGE_LOCAL $SAGE_DEVEL/sage
ln -sf $PWD/spkg/build/sage-%{version}/sage $SAGE_DEVEL/sage/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
# ensure proper/preferred libatlas is in linker path
pushd spkg/build/sage-%{version}
    perl -pi -e 's|^(extra_link_args = ).*|$1\["-L%{_libdir}/atlas"\]|;' sage/misc/cython.py
    # some .c files are not (re)generated
    find . \( -name \*.pyx -o -name \*.pxd \) | xargs touch
popd

# remove bundled jar files before build
rm spkg/build/extcode-%{version}/notebook/java/3d/lib/sage3d.jar \
   spkg/build/%{sagenb_pkg}/src/sagenb/sagenb/data/sage3d/lib/sage3d.jar

########################################################################
%build
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`
export DESTDIR=%{buildroot}
# Use file in /tmp because there are issues with long pathnames
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitearch}:$PYTHONPATH

%if %{with_sage_cython}
    pushd spkg/build/%{cython_pkg}/src
	%__python setup.py install --root=%{buildroot}
    popd
%endif

%if %{with_sage_ipython}
    pushd spkg/build/%{ipython_pkg}/src
	%__python setup.py install --root=%{buildroot}
    popd
%endif

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    pushd c_lib
	CXX=g++ UNAME=Linux SAGE64=auto scons
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
    make %{?_smp_mflags} CC="gcc -fPIC" CXX="g++ -fPIC" CFLAGS="%{optflags}"
popd

# last build command
rm -fr $DOT_SAGE

########################################################################
%install
export SAGE_ROOT=%{buildroot}%{SAGE_ROOT}
export SAGE_LOCAL=%{buildroot}%{SAGE_LOCAL}
export SAGE_DEVEL=%{buildroot}%{SAGE_DEVEL}
export SAGE_SHARE=%{buildroot}%{SAGE_SHARE}
export SAGE_EXTCODE=%{buildroot}%{SAGE_EXTCODE}
export SAGE_DOC=%{buildroot}%{SAGE_DOC}
export SAGE_PYTHONPATH=%{buildroot}%{SAGE_PYTHONPATH}
export DESTDIR=%{buildroot}
export DOT_SAGE=/tmp/sage$$
mkdir -p $DOT_SAGE/tmp

export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitearch}:$PYTHONPATH

#------------------------------------------------------------------------
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p $SAGE_PYTHONPATH
rm -fr $SAGE_DEVEL/sage $SAGE_LOCAL/{include,lib,share,notebook}
mkdir -p $SAGE_SHARE $SAGE_DOC $SAGE_LOCAL/bin $SAGE_DEVEL/sage
ln -sf $PWD/spkg/build/sage-%{version}/sage $SAGE_DEVEL/sage/sage
ln -sf %{_libdir} $SAGE_LOCAL/lib
ln -sf %{_includedir} $SAGE_LOCAL/include
ln -sf %{_datadir} $SAGE_LOCAL/share

#------------------------------------------------------------------------
# reinstall due to implicit clean
%if %{with_sage_cython}
    pushd spkg/build/%{cython_pkg}/src
	%__python setup.py install --root=%{buildroot}
    popd
    [ -f %{buildroot}%{_bindir}/cython ] &&
	mv -f %{buildroot}%{_bindir}/cython $SAGE_LOCAL/bin
    [ -d %{buildroot}%{python_sitearch}/Cython ] &&
	mv -f	%{buildroot}%{python_sitearch}/[Cc]ython*	\
		%{buildroot}%{SAGE_PYTHONPATH}
    # Do not override system cygdb
    mv %{buildroot}%{_bindir}/cygdb $SAGE_LOCAL/bin
%endif

#------------------------------------------------------------------------
# reinstall due to implicit clean
%if %{with_sage_ipython}
    pushd spkg/build/%{ipython_pkg}/src
	%__python setup.py install --root=%{buildroot}
    popd
    [ -f %{buildroot}%{_bindir}/%{ipython} &&
	mv -f %{buildroot}%{_bindir}/ipython $SAGE_LOCAL/bin
    rm -f	%{buildroot}%{_bindir}/ip*			\
		%{buildroot}%{_bindir}/irunner			\
		%{buildroot}%{_bindir}/pycolor
    [ -d %{buildroot}%{python_sitelib}/IPython ] &&
	mv -f	%{buildroot}%{python_sitelib}/IPython		\
		%{buildroot}%{python_sitelib}/ipython-*		\
		%{buildroot}%{SAGE_PYTHONPATH}
    rm -fr %{buildroot}%{_docdir}/ipython
    rm -f	%{buildroot}%{_mandir}/man1/ip*			\
		%{buildroot}%{_mandir}/man1/irunner*		\
		%{buildroot}%{_mandir}/man1/pycolor*
%endif

#------------------------------------------------------------------------
pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
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
    install -p -m755 %{SOURCE5} $SAGE_LOCAL/bin/testjava.sh
    # jmol
    rm -fr %{buildroot}%{python_sitearch}/sagenb/data/jmol

    mkdir -p %{buildroot}%{python_sitearch}/sagenb/data/jmol/appletweb
    pushd %{buildroot}%{python_sitearch}/sagenb/data/jmol
	cp -fa %{SOURCE3} %{SOURCE4} appletweb
%if 0%{?fedora}
	ln -s %{_javadir}/JmolApplet.jar .
%else
	ln -s %{_datadir}/jmol/JmolApplet.jar .
%endif
    popd

    # sage3d
    rm -f %{buildroot}%{_bindir}/sage3d
    ln -sf %{SAGE_LOCAL}/bin/sage3d %{buildroot}%{python_sitearch}/sagenb/data/sage3d/sage3d
    # flask stuff not installed
    cp -ar flask_version %{buildroot}%{python_sitearch}/sagenb
    ln -sf %{python_sitearch}/sagenb %{buildroot}%{SAGE_DEVEL}/sagenb
popd

#------------------------------------------------------------------------
%if %{with_sage_pexpect}
pushd spkg/build/%{pexpect_pkg}/src
    cp -f {ANSI,FSM,pexpect,pxssh,screen}.py $SAGE_PYTHONPATH
popd
%endif

#------------------------------------------------------------------------
%if %{with_sage_networkx}
pushd spkg/build/%{networkx_pkg}/src
    rm -fr $SAGE_PYTHONPATH/networkx*
    rm -fr %{buildroot}%{python_sitearch}/networkx*
    python setup.py install --root=%{buildroot} --install-purelib=%{SAGE_PYTHONPATH}
    rm -fr $SAGE_DOC/networkx*
    mv -f %{buildroot}/%{_datadir}/doc/* $SAGE_DOC
    rmdir %{buildroot}/%{_datadir}/doc
popd
%endif

#------------------------------------------------------------------------
cp -fa COPYING.txt $SAGE_ROOT
cp -far ipython $SAGE_ROOT
pushd spkg/build/sage_scripts-%{version}
    mkdir -p $SAGE_LOCAL/bin
    cp -fa sage-* *doctest.py ipy_profile_sage.py $SAGE_LOCAL/bin
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
%if !%{workaround_same_build_ID_in_nonidentical_files}
	dietz/cu2/cu2 \
%endif
	dik/dikcube \
	dik/size222 \
	$SAGE_LOCAL/bin
popd

#------------------------------------------------------------------------
rm -f %{buildroot}%{_bindir}/spkg-debian-maybe
pushd $SAGE_LOCAL/bin/
    rm -f sage-{bdist,build,build-debian,clone,crap,debsource,download_package,env,libdist,location,make_devel_packages,omega,pkg,pkg-nocompress,pull,push,sdist,sbuildhack,upgrade}
    rm -f sage-list-* sage-mirror* SbuildHack.pm sage-test-*
    rm -f sage-{verify-pyc,hardcode_sage_root,check-64,spkg*,update*,starts}
    rm -f *~
    rm -f sage-{check-libraries.py,ldwrap,open,osx-open,README-osx.txt}
    rm -f sage-rebase_sage.sh
    rm -f sage-{combinat,massif}
popd

#------------------------------------------------------------------------
pushd spkg/build/%{conway_polynomials_pkg}
    mkdir -p $SAGE_SHARE/conway_polynomials
    cp -fa src/conway_polynomials/* $SAGE_SHARE/conway_polynomials
popd

#------------------------------------------------------------------------
pushd spkg/build/%{elliptic_curves_pkg}
    python ./spkg-install
popd

#------------------------------------------------------------------------
pushd spkg/build/extcode-%{version}
    mkdir -p $SAGE_EXTCODE
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
	octave			\
	pari			\
	QEPCAD			\
	scilab			\
	singular		\
	sobj			\
	$SAGE_EXTCODE
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
export SAGE_DEVEL="$SAGE_DEVEL"
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
cat > %{buildroot}%{SAGE_LOCAL}/bin/sage3d << EOF
#!/bin/sh

java -classpath %{SAGE_DEVEL}/sage/sagenb/data/sage3d/lib/sage3d.jar:%{_javadir}/j3dcore.jar:%{_javadir}/vecmath.jar:%{_javadir}/j3dutils.jar org.sagemath.sage3d.ObjectViewerApp "\$1"
EOF
chmod +x %{buildroot}%{SAGE_LOCAL}/bin/sage3d

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
    %{buildroot}%{SAGE_DOC}/output/html/en/reference/todolist.html

#------------------------------------------------------------------------
# Fix links
rm -fr $SAGE_DEVEL/sage $SAGE_EXTCODE/sage $SAGE_ROOT/doc
ln -sf %{python_sitearch} $SAGE_DEVEL/sage
ln -sf %{python_sitearch} $SAGE_EXTCODE/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
rm -fr %{buildroot}%{python_sitearch}/site-packages

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

# Documentation is not rebuilt (also corrects rpmlint warning of hidden file)
find %{buildroot}%{SAGE_DOC} -name .buildinfo -exec rm {} \;

rm %{buildroot}%{python_sitearch}/sagenb/data/mathjax/.gitignore \
   %{buildroot}%{python_sitearch}/sagenb/data/mathjax/docs/.gitignore

# last install command
rm -fr $DOT_SAGE


########################################################################
%post		sagetex
%{_bindir}/mktexlsr

%postun		sagetex
%{_bindir}/mktexlsr

########################################################################
%files
%dir %{SAGE_ROOT}
%doc %{SAGE_ROOT}/COPYING.txt
%{SAGE_ROOT}/ipython
%dir %{SAGE_LOCAL}
%dir %{SAGE_LOCAL}/bin
%{SAGE_LOCAL}/bin/ipy_profile_sage.py
%{SAGE_LOCAL}/bin/ncadoctest.py
%{SAGE_LOCAL}/bin/QuadraticSieve
%{SAGE_LOCAL}/bin/gap_stamp
%if %{with_sage_cython}
%{SAGE_LOCAL}/bin/cython
%{SAGE_LOCAL}/bin/cygdb
%endif
%{SAGE_LOCAL}/bin/sage*
%{SAGE_LOCAL}/bin/testjava.sh
%{SAGE_LOCAL}/include
%{SAGE_LOCAL}/lib
%{SAGE_LOCAL}/share
%dir %{SAGE_DEVEL}
%{SAGE_PYTHONPATH}
%dir %{SAGE_SHARE}
%{_bindir}/sage
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

#------------------------------------------------------------------------
%files		core
%{SAGE_DEVEL}/sage
%{_libdir}/libcsage.so
%{python_sitearch}/sage
%{python_sitearch}/sage-*.egg-info

#------------------------------------------------------------------------
%files		data-conway_polynomials
%{SAGE_SHARE}/conway_polynomials

#------------------------------------------------------------------------
%files		data

#------------------------------------------------------------------------
%files		data-elliptic_curves
%{SAGE_SHARE}/cremona
%{SAGE_SHARE}/ellcurves

#------------------------------------------------------------------------
%files		data-extcode
%{SAGE_EXTCODE}

#------------------------------------------------------------------------
%files		data-graphs
%{SAGE_SHARE}/graphs

#------------------------------------------------------------------------
%files		data-polytopes_db
%{SAGE_SHARE}/reflexive_polytopes

#------------------------------------------------------------------------
%files		devel
%{_includedir}/csage

#------------------------------------------------------------------------
%files		doc
%{SAGE_ROOT}/doc
%dir %{SAGE_DOC}
%{SAGE_DOC}/common
%dir %{SAGE_DOC}/output
%dir %{SAGE_DOC}/output/html

#------------------------------------------------------------------------
%files		doc-de
%{SAGE_DOC}/de
%{SAGE_DOC}/output/html/de

#------------------------------------------------------------------------
%files		doc-en
%{SAGE_DOC}/en
%{SAGE_DOC}/output/html/en

#------------------------------------------------------------------------
%files		doc-fr
%{SAGE_DOC}/fr
%{SAGE_DOC}/output/html/fr

#------------------------------------------------------------------------
%files		doc-pt
%{SAGE_DOC}/pt
%{SAGE_DOC}/output/html/pt

#------------------------------------------------------------------------
%files		doc-ru
%{SAGE_DOC}/ru
%{SAGE_DOC}/output/html/ru

#------------------------------------------------------------------------
%files		doc-tr
%{SAGE_DOC}/tr
%{SAGE_DOC}/output/html/tr

#------------------------------------------------------------------------
%files		notebook
%{SAGE_DEVEL}/sagenb
%{python_sitearch}/sagenb
%{python_sitearch}/sagenb-*.egg-info

#------------------------------------------------------------------------
%files		rubiks
%{SAGE_LOCAL}/bin/optimal
%{SAGE_LOCAL}/bin/cubex
%{SAGE_LOCAL}/bin/mcube
%if !%{workaround_same_build_ID_in_nonidentical_files}
%{SAGE_LOCAL}/bin/cu2
%endif
%{SAGE_LOCAL}/bin/dikcube
%{SAGE_LOCAL}/bin/size222

#------------------------------------------------------------------------
%files		sagetex
%{python_sitearch}/sagetex*
%{_datadir}/texmf/tex/generic/sagetex
%doc %{_docdir}/%{sagetex_pkg}

########################################################################
%changelog
* Fri Jan 25 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.6-1
- Update to sagemath 5.6.
- Remove no longer required patch to build with system cython.

* Fri Jan 18 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.5-1
- Update to sagemath 5.5.

* Thu Dec 13 2012 <paulo.cesar.pereira.de.andrade@gmail.com> - 5.4.1-1
- Update to sagemath 5.4.1.

* Tue Nov 20 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.4-2
- Do not install alternate cygdb in %%_bindir
- Create the %{name}-core subpackage
- Create the %{name}-doc subpackage
- Create the %{name}-doc-en subpackage
- Create the %{name}-doc-de subpackage
- Create the %{name}-doc-fr subpackage
- Create the %{name}-doc-pt subpackage
- Create the %{name}-doc-ru subpackage
- Create the %{name}-doc-tr subpackage
- Create the %{name}-data metapackage
- Create the %{name}-data-conway_polynomials subpackage
- Create the %{name}-data-elliptic_curves subpackage
- Create the %{name}-data-extcode subpackage
- Do not install pickle_jar extcode contents
- Do not install notebook extcode contents
- Create the %{name}-data-graphs subpackage
- Create the %{name}-data-polytopes_db subpackage
- Create the %{name}-notebook subpackage
- Create the %{name}-rubiks subpackage
- Create the %{name}-sagetex subpackage

* Mon Nov 12 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.4-1
- Update to sagemath 5.4.
- Build with system networkx.
- Install only one fallback icon.
- Prevent rpm from providing private shared object.
- Change base directory to %%{_libdir} to avoid rpmlint errors.
- Correct permissions of installed shared objects.
- Rename most patches to use %%{name} prefix as "suggested" by fedora-review.
- Remove bundled jar files before %%build.
- Make cube solvers build optional and disabled by default.
- Add option to run "sage -testall" during package build.

* Sat Nov 10 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.4.beta1-4
- Add patch to make jmol export image functional
- Update pari patch to use proper path to gprc.expect
- Force usage of firefox in notebook (known to work are firefox and chromium)

* Tue Nov  6 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.4.beta1-1
- Update to sagemath 5.4.beta1
- Add Portuguese translations of Tutorial and A Tour of Sage
- Removed already applied upstream linbox upgrade patch
- Removed already applied upstream givaro upgrade patch
- Removed already applied upstream singular upgrade patch
- Install rubiks spkg binaries
- Use system genus2reduction

* Sat Aug 4 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.2-1
- Update to sagemath 5.2.

* Sun Jul 1 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.0.1-1
- Initial sagemath spec.
