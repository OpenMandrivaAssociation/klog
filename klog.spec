Name:           klog
Version:        1.9
Release:        1
Summary:	A Ham radio logging program for KDE
Group:		Communications
License:	GPLv2+
URL:            http://www.klog.xyz
Source0:        https://github.com/ea4k/klog/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        klog.desktop
#Patch0:         klog-1.2-fix-install.patch

BuildRequires:  dos2unix
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRequires:  qmake5
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:  pkgconfig(hamlib)
BuildRequires:  pkgconfig(Qt5Charts)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5PositioningQuick)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:  pkgconfig(Qt5SerialPort)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Widgets)

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

# For some reason all files in 0.9.2.9 are marked executable
find ./ -type f -exec chmod -x {} \;

%build
%qmake_qt5 \
         "PREFIX=%{buildroot}%{_prefix}" \
         "CONFIG+=debug c++14" \
         src/src.pro
%make_build

%install
%make_install

mv %{buildroot}%{_datadir}/%{name}/{COPYING,Changelog} .

# Install the provided desktop icon
for png in 48x48 64x64 128x128 256x256 512x512; do
  mkdir -p %{buildroot}%{_iconsdir}/hicolor/${png}/apps/
  convert -geometry $png src/img/klog_512x512.png %{buildroot}%{_iconsdir}/hicolor/${png}/apps/%{name}.png
done

# Install the provided desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%{_bindir}/%{name}
%doc Changelog README.md
%license COPYING
#{_datadir}/%{name}/translations/
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
#{_mandir}/man1/%{name}.1.*

