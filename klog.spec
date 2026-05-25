
Name:		klog
Version:	2.5.2
Release:	1
Summary:	A Ham radio logging program for KDE
Group:		Communications
License:	GPL-2.0-or-later
URL:		https://github.com/ea4k/klog
Source0:	https://github.com/ea4k/klog/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	make
BuildRequires:	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	hamlib++-devel
BuildRequires:	qmake-qt6
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(hamlib)
BuildRequires:	pkgconfig(Qt6Charts)
BuildRequires:	pkgconfig(Qt6Concurrent)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Location)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Positioning)
BuildRequires:	pkgconfig(Qt6PositioningQuick)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6QuickWidgets)
BuildRequires:	pkgconfig(Qt6SerialPort)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)

%description
KLog is a Ham radio logging program for KDE
Some features include:
	* DXCC award support.
	* Basic IOTA support.
	* Importing from Cabrillo files.
	* Importing from TLF.
	* Adding/Editing QSOs.
	* Save/read to/from disk file the log - ADIF format by default.
	* English/Spanish/Portuguese/Galician/Serbian/Swedish support.
	* QSL sent/received support.
	* Read/Write ADIF.
	* Delete QSOs.
	* DX-Cluster support. 
Some additional features of this application are still under development
and are not yet implemented.

%prep
%autosetup -n %{name}-%{version} -p1
# Fix dekstop file categories
sed -i 's/Categories=Utility;HamRadio;/Categories=Utility;Database;HamRadio;KDE/g' src/%{name}.desktop

%build
%cmake \
	-DCMAKE_BUILD_TYPE="RelWithDebInfo" \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# Install the provided desktop icons
for size in 16x16 24x24 32x32 48x48 64x64 128x128 256x256 512x512; do
    install -pDm 0644 images/%{name}_$size.png \
        %{buildroot}%{_datadir}/icons/hicolor/$size/apps/%{name}.png
done

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/translations/*.qm
%{_datadir}/pixmaps/%{name}.png
%{_docdir}/%{name}/*
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1.*
%{_metainfodir}/%{name}.metainfo.xml

