Summary:	QT plugin for SSL communications
Summary(pl):	Rozszerzenie QT do komunikacji po SSL
Name:		qt-plugin-ssl
Version:	1.0
Release:	4
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/qssl-%{version}.tar.bz2
Patch0:		%{name}-include.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	openssl-devel
BuildRequires:	sed
Requires:	qt >= 3.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	psi-qssl

%define		_xprefix	%{_prefix}/X11R6
%define		_xdatadir	%{_xprefix}/share

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
Requires:	openssl-devel

%description devel
QT plugin for SSL communications - headers.

%description devel -l pl
Rozszerzenie QT do komunikacji po SSL - pliki nag³ówkowe.

%prep
%setup -q -n qssl-%{version}
%patch0 -p2

%build
QTDIR=%{_xprefix}
export QTDIR
QMAKESPEC=%{_xdatadir}/qt/mkspecs/linux-g++
export QMAKESPEC

qmake qssl.pro
sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.tmp
mv -f Makefile.tmp Makefile

%{__make} \
	CXX=%{__cxx} \
	LINK=%{__cxx} \
	CXXFLAGS=" -pipe -Wall -W %{rpmcflags} -fno-rtti -fno-exceptions \
		-D_REENTRANT -fPIC %{!?debug:-DQT_NO_DEBUG} -DQT_THREAD_SUPPORT -DQT_PLUGIN"
mkdir mt
mv libqssl.so mt/
%{__make} clean
sed -e "s/thread/single/g" qssl.pro >> ./qssl.pro.tmp
mv -f qssl.pro.tmp qssl.pro
qmake qssl.pro
sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.tmp
mv -f Makefile.tmp Makefile
%{__make} \
	CXX=%{__cxx} \
	LINK=%{__cxx} \
	CXXFLAGS=" -pipe -Wall -W %{rpmcflags} -fno-rtti -fno-exceptions \
		-D_REENTRANT -fPIC %{!?debug:-DQT_NO_DEBUG} -DQT_THREAD_SUPPORT -DQT_PLUGIN"
mkdir st
mv libqssl.so st/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/qt/plugins-{mt,st}/network,%{_includedir}/qt}

install st/libqssl.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/network
install mt/libqssl.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network
install qssl*.h $RPM_BUILD_ROOT%{_includedir}/qt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/qt
