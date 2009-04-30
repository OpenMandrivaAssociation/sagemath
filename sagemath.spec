%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

%define		name			sagemath
%define		sagedir			%{_datadir}/%{name}
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
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{sagedatadir}

export DESTDIR=%{buildroot}

pushd spkg/build/sage-%{version}
    python setup.py install --root=%{buildroot}
    cp -fa c_lib/libcsage.so %{buildroot}%{_libdir}
popd

pushd spkg/build/sage_scripts-%{version}
    ./spkg-install
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

%clean
# rm -rf #%#{buildroot}

%files
%defattr(-,root,root)
%dir %{py_platsitedir}/sage
%{py_platsitedir}/*.egg-info
%{py_platsitedir}/sage/*
%dir %{sagedatadir}
%{sagedatadir}/*
%{_bindir}/*
%{_libdir}/*.so
