%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

%define		name			sagemath
%define		sagedir			%{_datadir}/sage
%define		sagedatadir		%{_localstatedir}/sage

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	3.2.3
Release:	%mkrel 1
Source0:	http://www.sagemath.org/src/sage-3.2.3.tar
URL:		http://www.sagemath.org/src/sage-3.2.3.tar
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gcc-gfortran

# BuildRequires:	ginac-devel
# It really wants the variant in pynac-0.1.1.spk,
# but an attempt on a python-ginac package from the sage spkg failed, as
# it depends on symbols that may or may not be available on the python binary,
# example:
#	py_acosh
# see http://mail.python.org/pipermail/python-bugs-list/2008-May/052722.html

BuildRequires:	libpari-devel
BuildRequires:	libatlas3
BuildRequires:	libblas-devel
BuildRequires:	libflint-devel
BuildRequires:	libfplll-devel
BuildRequires:	libm4ri-devel

# BuildRequires:	libpolybori-devel
# Need to use sage builtin one as it requires 0.5, but 0.6 was added to distro

BuildRequires:	libntl-devel
BuildRequires:	libqd-static-devel
BuildRequires:	libzn_poly-static-devel
BuildRequires:	linalg-linbox-devel
BuildRequires:	python-cython
BuildRequires:	python-setuptools
BuildRequires:	flex bison
BuildRequires:	singular-devel
BuildRequires:	libsymmetrica-static-devel
BuildRequires:	scons

# This is actually, mainly a listing of spkgs
Requires:	bzip2
Requires:	clisp
Requires:	ecm
## elliptic_curves-0.1.spkg
## extcode-3.2.3.spkg
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
Requires:	libatlas atlas
Requires:	libblas
Requires:	ntl
Requires:	libopencdk
Requires:	libm4ri-devel
Requires:	lcalc
Requires:	linalg-linbox
Requires:	maxima

# Requires:	mercurial

Requires:	moin
Requires:	libmpfi-devel
Requires:	palp
Requires:	perl
## polybori-0.5rc.p6.spkg
Requires:	polymake
## polytopes_db-20080430.spkg
Requires:	python
Requires:	python-cvxopt
Requires:	python-cython
Requires:	python-gd
Requires:	python-ghmm
Requires:	python-gnutls
Requires:	python-networkx
Requires:	python-matplotlib
Requires:	python-numpy
Requires:	python-pexpect
Requires:	python-pycrypto
Requires:	python-pygments
Requires:	python-processing
# scipy should also provide the weave (http://www.scipy.org/Weave) dependency
Requires:	python-scipy
Requires:	python-sphinx
Requires:	python-sqlalchemy
Requires:	python-sqlite2
Requires:	python-sympy
Requires:	python-twisted-core
Requires:	R-base
## rubiks-20070912.p8.spkg
Requires:	singular
Requires:	symmetrica
Requires:	sympow
Requires:	tachyon
## Requires:	zope

Patch0:		sage-3.2.3.patch
Patch1:		sage-3.2.3-sage_scripts.patch
Patch2:		sage-3.2.3-env-vars.patch

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.


########################################################################
%prep
%setup -q -n sage-%{version}

mkdir -p spkg/build
tar jxf spkg/standard/sage-%{version}.spkg -C spkg/build
tar jxf spkg/standard/sage_scripts-%{version}.spkg -C spkg/build
rm -f spkg/build/sage_scripts-%{version}/*.orig
tar jxf spkg/standard/conway_polynomials-0.2.spkg -C spkg/build
tar jxf spkg/standard/elliptic_curves-0.1.spkg -C spkg/build
tar jxf spkg/standard/extcode-3.2.3.spkg -C spkg/build

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export SAGE_ROOT=%{sagedir}
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`

export DESTDIR=%{buildroot}

pushd spkg/build/sage-%{version}
    pushd c_lib
	scons
    popd
    # some .c files are not (re)generated
    find . -name \*.pyx -exec touch {} \;
    python ./setup.py build
popd

%install
#rm -rf %#{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{sagedatadir}

export DESTDIR=%{buildroot}

pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
    mkdir -p %{buildroot}%{sagedir}/devel
    pushd sage
        find . -name \*.pxi -o -name \*.pxd -o -name \*.py -exec install -D -m 644 {} %{buildroot}%{sagedir}/devel/{} \;
    popd
popd

pushd spkg/build/sage_scripts-%{version}
    mkdir -p %{buildroot}%{sagedir}/bin
    cp -fa sage-* dsage_* *doctest.py ipy_profile_sage.py %{buildroot}%{sagedir}/bin
    cp -far ipython %{buildroot}%{sagedir}
    cp -fa matplotlibrc %{buildroot}%{sagedir}
    cp -fa COPYING.txt %{buildroot}%{sagedir}
    pushd %{buildroot}%{sagedir}/bin
	ln -sf %{_bindir}/python sage.bin
	ln -sf %{_bindir}/Singular sage_singular
	ln -sf %{_bindir}/gp sage_pari
    popd
popd

pushd spkg/build/conway_polynomials-0.2
    mkdir -p %{buildroot}%{sagedatadir}/conway_polynomials
    cp -fa src/conway_polynomials/* %{buildroot}%{sagedatadir}/conway_polynomials
popd

pushd spkg/build/elliptic_curves-0.1
    cp -fa cremona_mini/src/cremona_mini %{buildroot}%{sagedatadir}
    mkdir -p %{buildroot}%{sagedatadir}/ellcurves
    cp -fa ellcurves/rank* %{buildroot}%{sagedatadir}/ellcurves
popd

pushd spkg/build/extcode-3.2.3
    mkdir -p %{buildroot}%{sagedatadir}/extcode
    cp -far gap images javascript maxima mwrank notebook pari pickle_jar sagebuild singular \
	%{buildroot}%{sagedatadir}/extcode
popd

rm -f %{buildroot}%{_bindir}/spkg-debian-maybe

# not supported - only prebuilt packages for now
rm -f %{buildroot}%{sagedir}/bin/sage-bdist
rm -f %{buildroot}%{sagedir}/bin/sage-build
rm -f %{buildroot}%{sagedir}/bin/sage-build-debian
rm -f %{buildroot}%{sagedir}/bin/sage-clone
rm -f %{buildroot}%{sagedir}/bin/sage-crap
rm -f %{buildroot}%{sagedir}/bin/sage-debsource
rm -f %{buildroot}%{sagedir}/bin/sage-download_package
rm -f %{buildroot}%{sagedir}/bin/sage-env
rm -f %{buildroot}%{sagedir}/bin/sage-libdist
rm -f %{buildroot}%{sagedir}/bin/sage-list-*
rm -f %{buildroot}%{sagedir}/bin/sage-location
rm -f %{buildroot}%{sagedir}/bin/sage-make_devel_packages
rm -f %{buildroot}%{sagedir}/bin/sage-mirror*
# omega tool not available in mandriva version of valgrind
rm -f %{buildroot}%{sagedir}/bin/sage-omega
rm -f %{buildroot}%{sagedir}/bin/sage-pkg
rm -f %{buildroot}%{sagedir}/bin/sage-pkg-nocompress
rm -f %{buildroot}%{sagedir}/bin/sage-pull
rm -f %{buildroot}%{sagedir}/bin/sage-push
rm -f %{buildroot}%{sagedir}/bin/sage-sdist
rm -f %{buildroot}%{sagedir}/bin/SbuildHack.pm
rm -f %{buildroot}%{sagedir}/bin/sage-sbuildhack
rm -f %{buildroot}%{sagedir}/bin/sage-test-*
rm -f %{buildroot}%{sagedir}/bin/sage-upgrade

# osx only
rm -f %{buildroot}%{sagedir}/sage-check-libraries.py
rm -f %{buildroot}%{sagedir}/sage-ldwrap
rm -f %{buildroot}%{sagedir}/sage-native-execute
rm -f %{buildroot}%{sagedir}/sage-open
rm -f %{buildroot}%{sagedir}/sage-osx-open

# windows only
rm -f %{buildroot}%{sagedir}/sage-rebase_sage.sh

cat > %{buildroot}%{_bindir}/sage << EOF
#!/bin/sh

export SAGE_ROOT="/"
export SAGE_HOME="\$HOME/.sage/"
mkdir -p \$SAGE_HOME
export SAGE_DATA="%{sagedatadir}"
export SAGE_LOCAL="%{sagedir}"
export PATH=%{sagedir}/bin:\$PATH
%{sagedir}/bin/sage-sage $*
EOF
chmod +x %{buildroot}%{_bindir}/sage

%clean
# rm -rf #%#{buildroot}

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
