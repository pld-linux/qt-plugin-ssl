#
# Conditional build:
# _with_single		- build also single threaded library
#
Summary:	QT plugin for SSL communications
Summary(pl):	Rozszerzenie QT do komunikacji po SSL
Name:		qt-plugin-ssl
Version:	2.0
Release:	2
License:	GPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/psi/qssl-%{version}.tar.bz2
# Source0-md5:	2593eb1e979070edcd07e10442f117dc
URL:		http://psi.affinix.com/
BuildRequires:	openssl-devel >= 0.9.6j
BuildRequires:	qt-devel >= 3.1.2
Requires:	qt >= 3.1.2
%{?_with_single:Requires:	qt-st}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	psi-qssl

%define		_prefix		/usr/X11R6
%define		_includedir	%{_prefix}/include/qt

%description
QT plugin for SSL communications.

%description -l pl
Rozszerzenie QT do komunikacji po SSL.

%package devel
Summary:	QT plugin for SSL communications - headers
Summary(pl):	Rozszerzenie QT do komunikacji po SSL - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	qt-devel >= 3.1.2
Requires:	openssl-devel >= 0.9.6j

%description devel
QT plugin for SSL communications - headers.

%description devel -l pl
Rozszerzenie QT do komunikacji po SSL - pliki nag³ówkowe.

%prep
%setup -q -n qssl-%{version}

%build
export QTDIR=%{_prefix}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++

qmake qssl.pro

sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.tmp
mv -f Makefile.tmp Makefile

%{__make} \
	CXX=%{__cxx} \
	LINK=%{__cxx} \
	CXXFLAGS=" \
	-pipe \
	-Wall \
	-W %{rpmcflags} \
	-fno-rtti \
	-fno-exceptions \
	-D_REENTRANT \
	-fPIC \
	%{!?debug:-DQT_NO_DEBUG} \
	-DQT_THREAD_SUPPORT \
	-DQT_PLUGIN"

mkdir mt
mv libqssl.so mt
%{__make} clean

%if %{?_with_single:1}0
sed -e "s/thread/single/g" qssl.pro >> ./qssl.pro.tmp
mv -f qssl.pro.tmp qssl.pro

qmake qssl.pro

sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.tmp
mv -f Makefile.tmp Makefile

%{__make} \
	CXX=%{__cxx} \
	LINK=%{__cxx} \
	CXXFLAGS=" \
	-pipe \
	-Wall \
	-W %{rpmcflags} \
	-fno-rtti \
	-fno-exceptions \
	-D_REENTRANT \
	-fPIC \
	%{!?debug:-DQT_NO_DEBUG} \
	-DQT_THREAD_SUPPORT \
	-DQT_PLUGIN"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network \
	%{?_with_single:$RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/network} \
	$RPM_BUILD_ROOT%{_includedir}

install mt/libqssl.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network

%if %{?_with_single:1}0
install libqssl.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/network
%endif

install qssl*.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/qt/plugins-?t/network/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
