%define name    klog
%define version 0.5.7
%define rel     1


Name:           %{name}
Version:        %{version}
Release:        %mkrel %{rel}
Summary:	A Ham radio logging program for KDE

Group:		Communications
License:	GPLv2+
URL:		http://jaime.robles.es/eklog.php
Source0:	http://jaime.robles.es/%{name}/download/%{name}-%{version}.tar.gz
# Wrapper script installs needed files in users home directory.
Source1:	%{name}.sh.in
# Patch CMakeLists.txt
#Patch0:		%{name}-%{version}.CMakeList.txt.patch
# Patch .desktop file
#Patch1:		%{name}-%{version}.desktop.patch


BuildRequires:	qt4-devel
BuildRequires:	hamlib-devel
BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++

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
%setup -q
#%patch0 -p1 -b %{name}-%{version}.CMakeList.txt.patch
#%patch1 -p1 -b %{name}-%{version}.desktop.patch

%build
%cmake   -DCMAKE_INSTALL_PREFIX=/usr

%make     CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C build

%find_lang %{name}


# Install default user configuration files
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/data/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/awa/
install -p -D -m 0644 ./awa/tpea.awa $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/awa/tpea.awa
install -p -D -m 0644 ./awa/was.awa $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/awa/was.awa
install -p -D -m 0644 ./data/cty.dat $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/data/cty.dat
install -p -D -m 0644 ./data/%{name}-contest-cabrillo-formats.txt $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.%{name}/data/%{name}-contest-cabrillo-formats.txt

# Install the provided .desktop icon
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/pixmaps/
install -p -D -m 0644 ./icons/%{name}-icon.png $RPM_BUILD_ROOT/%{_datadir}/pixmaps/%{name}-icon.png

desktop-file-install \
	--dir=$RPM_BUILD_ROOT%{_datadir}/applications/kde4 \
	$RPM_BUILD_ROOT/%{_datadir}/applications/kde4/%{name}.desktop

# Move original binary to libexecdir
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/
mv $RPM_BUILD_ROOT/%{_bindir}/%{name} $RPM_BUILD_ROOT/%{_libexecdir}/%{name}-bin

# Install wrapper script installs needed files in users home directory.
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README TODO NEWS
%{_bindir}/%{name}
%{_libexecdir}/%{name}-bin
%{_datadir}/pixmaps/%{name}-icon.png
%{_datadir}/applications/kde4/%{name}.desktop
%{_datadir}/icons/locolor/16x16/apps/%{name}.png
%{_datadir}/icons/locolor/32x32/apps/%{name}.png
%{_datadir}/apps/%{name}/klogui.rc
%dir %{_sysconfdir}/skel/.%{name}/
%dir %{_sysconfdir}/skel/.%{name}/data/
%dir %{_sysconfdir}/skel/.%{name}/awa/
%config(noreplace) %{_sysconfdir}/skel/.%{name}/data/%{name}-contest-cabrillo-formats.txt
%config(noreplace) %{_sysconfdir}/skel/.%{name}/data/cty.dat
%config(noreplace) %{_sysconfdir}/skel/.%{name}/awa/was.awa
%config(noreplace) %{_sysconfdir}/skel/.%{name}/awa/tpea.awa


