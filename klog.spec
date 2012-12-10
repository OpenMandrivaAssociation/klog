%define name    klog
%define version 0.5.9
%define rel     1

Name:           %{name}
Version:        %{version}
Release:        %mkrel %{rel}
Summary:	A Ham radio logging program for KDE

Group:		Communications
License:	GPLv2+
URL:		http://jaime.robles.es/eklog.php
Source0:	http://jaime.robles.es/download/%{name}-%{version}.tar.gz
# Wrapper script installs needed files in users home directory.
Source1:	%{name}.sh.in
BuildRequires:	kdelibs4-devel
BuildRequires:	hamlib-devel
BuildRequires:	desktop-file-utils

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

sed -i -e 's#/usr/libexec#%{_libexecdir}#' %{SOURCE1}

%build
%cmake_kde4
%make

%install
%makeinstall_std -C build

%find_lang %{name}

# Install default user configuration files
mkdir -p %{buildroot}/%{_sysconfdir}/skel/.%{name}/data/
mkdir -p %{buildroot}/%{_sysconfdir}/skel/.%{name}/awa/
install -p -D -m 0644 ./awa/tpea.awa %{buildroot}/%{_sysconfdir}/skel/.%{name}/awa/tpea.awa
install -p -D -m 0644 ./awa/was.awa %{buildroot}/%{_sysconfdir}/skel/.%{name}/awa/was.awa
install -p -D -m 0644 ./data/cty.dat %{buildroot}/%{_sysconfdir}/skel/.%{name}/data/cty.dat
install -p -D -m 0644 ./data/%{name}-contest-cabrillo-formats.txt %{buildroot}/%{_sysconfdir}/skel/.%{name}/data/%{name}-contest-cabrillo-formats.txt

# Install the provided .desktop icon
mkdir -p %{buildroot}/%{_datadir}/pixmaps/
install -p -D -m 0644 ./icons/%{name}-icon.png %{buildroot}/%{_datadir}/pixmaps/%{name}-icon.png

desktop-file-install \
	--dir=%{buildroot}%{_datadir}/applications/kde4 \
	%{buildroot}/%{_datadir}/applications/kde4/%{name}.desktop

# Move original binary to libexecdir
mkdir -p %{buildroot}/%{_libexecdir}/
mv %{buildroot}/%{_bindir}/%{name} %{buildroot}/%{_libexecdir}/%{name}-bin

# Install wrapper script installs needed files in users home directory.
install -p -D -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/%{name}

%files -f %{name}.lang
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
