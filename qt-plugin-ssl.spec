Summary:	QT plugin for SSL communications
Summary(pl):	Rozszerzenie QT do komunikacji po SSL
Name:		qssl
Version:	1.0
Release:	4
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/%{name}-%{version}.tar.bz2
Patch0:		%{name}-include.patch
URL:		http://psi.affinix.com
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	openssl-devel
Requires:	qt >= 3.0.5
Requires:	openssl
BuildRequires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	psi-qssl

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
QT plugin for SSL communications.

%description -l pl
Rozszerzenie QT do komunikacji po SSL.

%package devel
Summary:	QT plugin for SSL communications - headers
Summary(pl):	Rozszerzenie QT do komunikacji po SSL - pliki nagłówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	qt-devel >= 3.0.5
Requires:	openssl-devel

%description devel
QT plugin for SSL communications - headers.

%description devel -l pl
Rozszerzenie QT do komunikacji po SSL - pliki nagłówkowe.

%prep
%setup -q
%patch0 -p2

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

qmake qssl.pro
sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.1
mv -f Makefile.1 Makefile

%{__make}
mkdir mt
mv libqssl.so mt/
%{__make} clean
sed -e "s/thread/single/g" qssl.pro >> ./qssl.pro.1
mv -f qssl.pro.1 qssl.pro
qmake qssl.pro
sed -e "s/\,libqssl\.so\.1/\,libqssl\.so/g" Makefile >> Makefile.1
mv -f Makefile.1 Makefile
%{__make}
mkdir st
mv libqssl.so st/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_libdir}/qt
install -d $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/
install -d $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/network
install -d $RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/
install -d $RPM_BUILD_ROOT%{_libdir}/qt/plugins-st/network
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_includedir}/qt

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
