%global with_sphinx_hack	1

# may be required if not matching system version or to be updates proof
%global with_sage_cython	1

# ipython-0.11 drastically changed api since ipython-0.10.2
%global with_sage_ipython	1

# sagemath uses a somewhat old and heavily patched networkx
%global with_sage_networkx	1

# sagemath works only with pexpect-2.0
%global with_sage_pexpect	1

%global conway_polynomials_pkg	conway_polynomials-0.2
%global cython_pkg		cython-0.17pre
%global	elliptic_curves_pkg	elliptic_curves-0.6
%global	flintqs_pkg		flintqs-20070817.p8
%global graphs_pkg		graphs-20120404.p3
%global ipython_pkg		ipython-0.10.2.p1
%global networkx_pkg		networkx-1.6
%global pexpect_pkg		pexpect-2.0.p5
%global polytopes_db_pkg	polytopes_db-20100210.p1
%global rubiks_pkg		rubiks-20070912.p18
%global	sagenb_pkg		sagenb-0.10.2
%global sagetex_pkg		sagetex-2.3.3.p2

%global SAGE_ROOT		%{_datadir}/sagemath
%global SAGE_LOCAL		%{SAGE_ROOT}/local
%global SAGE_DEVEL		%{SAGE_ROOT}/devel
%global SAGE_DOC		%{SAGE_DEVEL}/doc
%global SAGE_DATA		%{SAGE_ROOT}/data
%global SAGE_PYTHONPATH		%{SAGE_ROOT}/site-packages

Name:		sagemath
Group:		Sciences/Mathematics
Summary:	A free open-source mathematics software system
Version:	5.4.beta1
Release:	1
License:	GPL
URL:		http://www.sagemath.org
Source0:	http://www.sagemath.org/src/sage-%{version}.tar
Source1:	gprc.expect
Source2:	makecmds.sty
Source3:	%{name}.rpmlintrc

Patch0:		sage-gmp.patch
Patch1:		sage-scripts.patch

# remove call to not implemented sagemath "is_package_installed" interfaces
# mpc is available in all modern linux distros
# need to package coin-or solver in fedora
# remove check for non free solvers
Patch3:		sage-extensions.patch

# helper to:
#	o respect a DESTDIR environment variable
#	o avoid double '//' in pathnames, what can confused debugedit & co
#	o minor change to help in incremental builds by avoiding rebuilding
#	  files
#	o do not assume there is an installed sagemath
Patch4:		sage-rpmbuild.patch

# build documentation in buildroot environment
Patch5:		sage-sagedoc.patch

# sage notebook rpm and system environment adjustments
Patch6:		sage-sagenb.patch

# do not attempt to create state files in system directories
Patch7:		sage-readonly.patch

# force coercion of ecl t_string to ecl t_base_string
# this is hackish and only required if ecl is built with unicode support
Patch8:		sage-ecl-unicode.patch

# do not link explicitly to png12
Patch9:		sage-png.patch

# work with all maxima-runtime lisp backend packages
Patch10:	sage-maxima.patch

# execute 4ti2 programs in $PATH not in $SAGE_ROOT/local/bin
Patch11:	sage-4ti2.patch

Patch12:	sage-fplll.patch

Patch13:	sage-qepcad.patch
Patch14:	sage-pari.patch
Patch15:	sage-networkx.patch
Patch16:	sage-lie.patch
Patch17:	sage-gap.patch

# Portuguese translations: http://trac.sagemath.org/sage_trac/ticket/12822
Patch18:	trac_12502_pt_translation_of_a_tour_of_sage_rebase1.patch
Patch19:	trac_12822_pt_translation_of_tutorial.patch
Patch20:	trac_12822_pt_translation_of_tutorial_rev1.patch

BuildRequires:	boost-devel
BuildRequires:	cliquer-devel
BuildRequires:	dos2unix
BuildRequires:	factory-devel
BuildRequires:	flint-devel
BuildRequires:	fplll-devel
BuildRequires:	ecl
BuildRequires:	eclib-devel
BuildRequires:	ecm-devel
BuildRequires:	gap-system
BuildRequires:	gap-system-packages
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
BuildRequires:	python-numpy-devel
BuildRequires:	python-scipy
BuildRequires:	python-twisted
BuildRequires:	polybori-devel
BuildRequires:	ratpoints
BuildRequires:	readline-devel
BuildRequires:	scons
BuildRequires:	singular-devel
BuildRequires:	symmetrica-devel

Requires:	4ti2
Requires:       cddlib-devel
Requires:	ecl
Requires:	gap-system
Requires:	gap-system-packages
Requires:	genus2reduction
Requires:	gfan
Requires:	gp2c
Requires:	iml-devel
Requires:	jmol
Requires:	jsmath-fonts
Requires:	libpari-devel
Requires:	maxima-gui
Requires:	maxima-runtime-ecl
Requires:	palp
Requires:	pari
Requires:	pari-data
Requires:	python-pycrypto
Requires:	python-cvxopt
Requires:	python-flask-autoindex
Requires:	python-flask-babel
Requires:	python-flask-openid
Requires:	python-flask-silk
Requires:	python-sympy
Requires:	python-twisted-web
Requires:	python-twisted-web2
Requires:	R
Requires:	singular
Requires:	sympow
Requires:	tachyon

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.

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
%patch15 -p1
%patch16 -p1
%patch17 -p1

pushd spkg/build/sage-%{version}
mkdir -p doc/pt/a_tour_of_sage/
cp -fa doc/en/a_tour_of_sage/*.png doc/pt/a_tour_of_sage/
%patch18 -p1
%patch19 -p1
%patch20 -p1
popd

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

#------------------------------------------------------------------------
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
export SAGE_DATA=%{buildroot}%{SAGE_DATA}
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
mkdir -p $SAGE_DATA $SAGE_DOC $SAGE_LOCAL/bin $SAGE_DEVEL/sage
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
    rm -f %{buildroot}%{python_sitearch}/sagenb/data/jmol
    rm -f %{buildroot}%{python_sitearch}/sagenb/data/sage3d/sage3d
    python setup.py install --root=%{buildroot} --install-purelib=%{python_sitearch}
    # will install sage3d a proper sage3d below
    rm -f %{buildroot}%{_bindir}/sage3d
    # remove duplicated jmol that only works with sage
    rm -f %{buildroot}%{_bindir}/jmol
    rm -fr %{buildroot}%{python_sitearch}/sagenb/data/jmol
    # use system jmol
    ln -sf %{_javadir} %{buildroot}%{python_sitearch}/sagenb/data/jmol
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
install -m755 spkg/bin/sage $SAGE_LOCAL/bin

#------------------------------------------------------------------------
pushd spkg/build/%{flintqs_pkg}/src
    cp -fa QuadraticSieve $SAGE_LOCAL/bin
popd

#------------------------------------------------------------------------
# FIXME create proper package(s) for cube solvers
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
rm -f %{buildroot}%{_bindir}/spkg-debian-maybe
pushd $SAGE_LOCAL/bin/
    rm -f sage-{bdist,build,build-debian,clone,crap,debsource,download_package,env,libdist,location,make_devel_packages,omega,pkg,pkg-nocompress,pull,push,sdist,sbuildhack,upgrade}
    rm -f sage-list-* sage-mirror* SbuildHack.pm sage-test-*
    rm -f sage-{verify-pyc,hardcode_sage_root,check-64,spkg*,update*,starts}
    rm -f *~
    rm -f sage-{check-libraries.py,ldwrap,open,osx-open,README-osx.txt}
    rm -f sage-rebase_sage.sh
    rm -f sage-combinat
popd


#------------------------------------------------------------------------
pushd spkg/build/%{conway_polynomials_pkg}
    mkdir -p $SAGE_DATA/conway_polynomials
    cp -fa src/conway_polynomials/* $SAGE_DATA/conway_polynomials
popd

#------------------------------------------------------------------------
pushd spkg/build/%{elliptic_curves_pkg}
    python ./spkg-install
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
    cp -f %{SOURCE1} $SAGE_DATA/extcode/pari
popd

#------------------------------------------------------------------------
pushd spkg/build/%{graphs_pkg}
    mkdir -p $SAGE_DATA/graphs
    cp -fa src/* $SAGE_DATA/graphs
popd

#------------------------------------------------------------------------
pushd spkg/build/%{polytopes_db_pkg}
    mkdir -p $SAGE_DATA/reflexive_polytopes
    cp -fa src/* $SAGE_DATA/reflexive_polytopes
popd

#------------------------------------------------------------------------
pushd spkg/build/%{sagetex_pkg}/src
    python setup.py install --root=%{buildroot} --install-purelib=%{python_sitearch}
    install -m 0644 -D %{SOURCE2} \
	%{buildroot}%{_datadir}/texmf/tex/generic/sagetex/makecmds.sty
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
export SAGE_DATA="$SAGE_DATA"
export SAGE_DEVEL="$SAGE_DEVEL"
##export SAGE_DOC="$SAGE_DOC"
export PATH=$SAGE_LOCAL/bin:%{_libdir}/4ti2/bin:\$PATH
export SINGULARPATH=%{_libdir}/Singular/LIB
export SINGULAR_BIN_DIR=%{_libdir}/Singular
##export PYTHONPATH="$SAGE_PYTHONPATH"
export SAGE_CBLAS=cblas
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=\`gfortran --print-file-name=libgfortran.so\`
export SYMPOW_DIR="\$DOT_SAGE/sympow"
export LC_MESSAGES=C
export LC_NUMERIC=C
MALLOC_CHECK_=1 $SAGE_LOCAL/bin/sage "\$@"
EOF
#------------------------------------------------------------------------
chmod +x %{buildroot}%{_bindir}/sage

#------------------------------------------------------------------------
cat > %{buildroot}%{_datadir}/sagemath/local/bin/sage3d << EOF
#!/bin/sh

java -classpath %{SAGE_DEVEL}/sage/sagenb/data/sage3d/lib/sage3d.jar:%{_javadir}/j3dcore.jar:%{_javadir}/vecmath.jar:%{_javadir}/j3dutils.jar org.sagemath.sage3d.ObjectViewerApp "\$1"
EOF
chmod +x %{buildroot}%{_datadir}/sagemath/local/bin/sage3d

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
	install -D -m 0644 $f %{buildroot}/%{python_sitearch}/$f
    done
    # need this or will not "find" the files in the directory, and
    # fail to link with gmp
    touch %{buildroot}/%{python_sitearch}/sage/libs/gmp/__init__.py
popd

#------------------------------------------------------------------------
%if %{with_sage_pexpect}
    cp -f $SAGE_PYTHONPATH/{ANSI,FSM,pexpect,pxssh,screen}.py %{buildroot}%{python_sitearch}
%endif

# Build documentation, using %{buildroot} environment
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

%if %{with_sage_pexpect}
    rm -f %{buildroot}%{python_sitearch}/{ANSI,FSM,pexpect,pxssh,screen}.py
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
rm -fr $SAGE_DEVEL/sage $SAGE_DATA/extcode/sage $SAGE_ROOT/doc
ln -sf %{python_sitearch} $SAGE_DEVEL/sage
ln -sf %{python_sitearch} $SAGE_DATA/extcode/sage
ln -sf %{SAGE_DOC} $SAGE_ROOT/doc
rm -fr %{buildroot}%{python_sitearch}/site-packages

# Install menu and icons
pushd spkg/build/extcode-%{version}
    install -m644 -D notebook/images/icon16x16.png %{buildroot}%{_miconsdir}/%{name}.png
    install -m644 -D notebook/images/icon32x32.png %{buildroot}%{_iconsdir}/%{name}.png
    install -m644 -D notebook/images/icon32x32.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
    install -m644 -D notebook/images/icon48x48.png %{buildroot}%{_liconsdir}/%{name}.png
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

# last install command
rm -fr $DOT_SAGE


########################################################################
%post
%{_bindir}/mktexlsr

%postun
%{_bindir}/mktexlsr

########################################################################
%files
%{python_sitearch}/*
%{SAGE_ROOT}
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/csage
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}*.png
%{_miconsdir}/%{name}*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/texmf/tex/generic/sagetex
%{_docdir}/sagetex

%changelog
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
