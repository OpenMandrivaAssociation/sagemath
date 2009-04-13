%define		_enable_debug_packages	%{nil}
%define		debug_package		%{nil}

%define		name			sagemath
%define		sagedir			%{_datadir}/%{name}
%define		sagedatadir		%{sagedir}/data

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	A free open-source mathematics software system
Version:	3.2.3
Release:	%mkrel 1
Source0:	http://www.sagemath.org/src/sage-3.2.3.tar
URL:	http://www.sagemath.org/src/sage-3.2.3.tar
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
Requires:	gfortran
Requires:	gp2c pari pari-data pari-devel
## graphs-20070722.spkg 
Requires:	ipython
Requires:	jmol
Requires:	libatlas atlas
Requires:	libblas
Requires:	libntl
Requires:	libopencdk
Requires:	libm4ri
Requires:	lcalc
Requires:	linalg-linbox
Requires:	maxima
Requires:	mercurial
Requires:	moin
Requires:	mpfi
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
Requires:	zope


Patch0:		sage-3.2.3.patch

%description
Sage is a free open-source mathematics software system licensed
under the GPL. It combines the power of many existing open-source
packages into a common Python-based interface.


########################################################################
%prep
%setup -q -n sage-%{version}

mkdir -p spkg/build
tar jxf spkg/standard/sage-%{version}.spkg -C spkg/build

%patch0 -p1

%build
export SAGE_ROOT=%{sagedir}
export SAGE_FORTRAN=%{_bindir}/gfortran
export SAGE_FORTRAN_LIB=`gfortran --print-file-name=libgfortran.so`

export BUILDROOT=%{buildroot}

pushd spkg/build
    cd sage-%{version}
    python setup.py build
popd

%install
rm -rf %{buildroot}

pushd spkg/build
    python setup.py install
popd

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{sagedatdir}

mkdir -p %{buildroot}%{sagedatadir}/conway_polynomials
cp conway_polynomials-0.2/src/conway_polynomials/conway_table.py.bz2 %{buildroot}%{sagedatadir}/conway_polynomials
bunzip2 %{buildroot}%{sagedatadir}/conway_polynomials/conway_table.py.bz2

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
