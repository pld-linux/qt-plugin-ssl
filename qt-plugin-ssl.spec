#
# Conditional build:
%bcond_with	single	# build also single threaded library (deprecated)
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
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qt-devel >= 3.0.5
%{?with_single:BuildRequires:	qt-st-devel >= 3.0.5}
Requires:	qt >= 3.0.5
%{?with_single:Requires:	qt-st >= 3.0.5}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	psi-qssl

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
Requires:	qt-devel >= 3.0.5
Requires:	openssl-devel >= 0.9.7c

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
	CXX="%{__cxx}" \
	LINK="%{__cxx}" \
	CXXFLAGS="-pipe -Wall -W %{rpmcflags} -fPIC -fno-rtti -fno-exceptions \
	-D_REENTRANT %{!?debug:-DQT_NO_DEBUG} -DQT_THREAD_SUPPORT -DQT_PLUGIN" \
	LDFLAGS="%{rpmldflags} -shared"

mkdir mt
mv libqssl.so mt
%{__make} clean

%if %{with single}
sed -e "s/thread/single/g" qssl.pro >> ./qssl.pro.tmp
mv -f qssl.pro.tmp qssl.pro

qmake qssl.pro

sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.tmp
mv -f Makefile.tmp Makefile

%{__make} \
	CXX="%{__cxx}" \
	LINK="%{__cxx}" \
	CXXFLAGS=" -pipe -Wall -W %{rpmcflags} -fPIC -fno-rtti -fno-exceptions \
	-D_REENTRANT %{!?debug:-DQT_NO_DEBUG} -DQT_PLUGIN" \
	LFLAGS="%{rpmldflags} -shared"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network \
	%{?with_single:$RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/network} \
	$RPM_BUILD_ROOT%{_includedir}

install mt/libqssl.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network

%if %{with single}
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
