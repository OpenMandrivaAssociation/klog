# NOTE Upstream is working on a v2.5.n series which should be fully ported to CMake
# NOTE which will hopefully mean having to patch it less downstream.
# NOTE This GH issue milestone is tracking that work:
# NOTE https://github.com/ea4k/klog/issues?q=milestone%3AKLog-2.5

Name:		klog
Version:	2.4.3
Release:	1
Summary:	A Ham radio logging program for KDE
Group:		Communications
License:	GPL-2.0-or-later
URL:		https://www.klog.xyz
Source0:	https://github.com/ea4k/klog/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:	klog.desktop

BuildRequires:	cmake
BuildRequires:	make
BuildRequires:	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	gettext
BuildRequires:	hamlib++-devel
BuildRequires:	qmake-qt6
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6ExamplesAssetDownloaderPrivate)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(hamlib)
BuildRequires:	pkgconfig(Qt6Charts)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Location)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Positioning)
BuildRequires:	pkgconfig(Qt6PositioningQuick)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6QmlAssetDownloader)
BuildRequires:	pkgconfig(Qt6QuickWidgets)
BuildRequires:	pkgconfig(Qt6SerialPort)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Xml)

#BuildRequires:	glibc-static-devel

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
%autosetup -p1 -n %{name}-%{version}

# Fix line endings
dos2unix TODO

%build
#export CFLAGS="%%{optflags} -fno-lto -Wno-error=deprecated-declarations -Wno-error=unused-result"
export QMAKE_CXXFLAGS="%{optflags} -fno-lto -Wno-error=deprecated-declarations -Wno-error=unused-result"
qmake-qt6  \
	PREFIX=%{buildroot}%{_prefix} \
	"CONFIG+=debug c++17" \
	src/src.pro
#%%cmake \
#	-DCMAKE_INSTALL_PREFIX=/usr/ \
#	-G Ninja

%make_build

%install
%make_install

mv %{buildroot}%{_datadir}/%{name}/{COPYING,Changelog} .

# Install the provided desktop icon
for size in 16x16 24x24 32x32 48x48 64x64 128x128 256x256 512x512; do
    install -pDm 0644 images/%{name}_$size.png \
        %{buildroot}%{_datadir}/icons/hicolor/$size/apps/%{name}.png
done

# Install the provided desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

# Install man page
install -Dpm 644 src/%{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1

# Install the translations qm files from lrelease translations/*.ts
install -dp %{buildroot}/%{_datadir}/klog/translations
install -pm 644 build/target/translations/*.qm %{buildroot}/%{_datadir}/klog/translations

%files
%{_bindir}/%{name}
%doc Changelog README.md
%license COPYING
%{_datadir}/%{name}/translations/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/klog/mapqmlfile.qml
%{_datadir}/klog/marker.qml
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1.*

