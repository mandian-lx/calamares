%global snapdate 20150112

%define major 0
%define libname %mklibname %{name} {major}
%define develname %mklibname %{name} -d

Summary:	Distribution-independent installer framework 
Name:		calamares
Version:	0.17.0
Release:	0.%{snapdate}.1
Group:		System/Configuration/Other
License:	GPLv3+
URL:		http://calamares.io/
# git archive --format=tar --prefix=calamares-0.17.0-20150112/ HEAD | xz -vf > calamares-0.17.0-20150112.tar.xz
Source0:	calamares-%{version}-%{snapdate}.tar.xz
Patch0:         calamares-0.17.0-20150112-openmandriva-settings.patch
Patch1:         calamares-0.17.0-20150112-openmandriva-desktop-file.patch
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(libatasmart)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(polkit-qt5-1)
BuildRequires:	cmake >= 3.0
BuildRequires:	cmake(ECM)
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5Solid)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
Requires(post):	distro-release-OpenMandriva
Requires(post):	distro-theme-OpenMandriva
Requires:	coreutils
Requires:	util-linux
Requires:	dracut
Requires:	grub2
%ifarch x86_64
# EFI currently only supported on x86_64
Requires:       grub2-efi
%endif
Requires:	console-setup
# x11 stuff
Requires:	setxkbmap
Requires:	xkbcomp
Requires:	NetworkManager
Requires:	os-prober
Requires:	e2fsprogs
Requires:	dosfstools
Requires:	ntfs-3g
Requires:	gawk
#(tpg) needs to be ported to KF5
#Requires:	partitionmanager
Requires:	systemd
Requires:	systemd-units
Requires:	rsync
Requires:	shadow
Requires:	polkit
Requires:       urpmi
ExclusiveArch:	%{ix86} x86_64

%description
Calamares is a distribution-independent installer framework,
designed to install from a live CD/DVD/USB environment to
a hard disk. It includes a graphical installation
program based on Qt 5.

%package -n %{libname}
Summary:	Calamares runtime libraries
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Librarief for %{name}.


%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C 
Requires:	%{libname} = %{EVRD}
Requires:	cmake

%description -n %{develname}
Development files and headers for %{name}.


%prep
%setup -q -n %{name}-%{version}-%{snapdate}

%patch0 -p1 -b .default-settings
%patch1 -p1 -b .desktop-file

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build
%cmake_qt5 -DWITH_PARTITIONMANAGER:BOOL="OFF" -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"

%make

%install
%makeinstall_std

#own the auto branding directory
mkdir -p %{buildroot}%{_datadir}/calamares/branding/auto
touch %{buildroot}%{_datadir}/calamares/branding/auto/branding.desc

#own the local settings directories
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding

%post
# generate the "auto" branding
. %{_sysconfdir}/os-release

cat >%{_datadir}/calamares/branding/auto/branding.desc <<EOF
# THIS FILE IS AUTOMATICALLY GENERATED! ANY CHANGES TO THIS FILE WILL BE LOST!
---
componentName:  auto

strings:
    productName:         "$NAME"
    shortProductName:    "$NAME"
    version:             "$VERSION"
    shortVersion:        "$VERSION_ID"
    versionedName:       "$NAME $VERSION"
    shortVersionedName:  "$NAME $VERSION_ID"
    bootloaderEntryName: "$NAME"

images:
    productLogo:         "%{_iconsdir}/openmandriva.svg"
    productIcon:         "%{_iconsdir}/openmandriva.svg"

slideshow:
    - "%{_iconsdir}/openmandriva.svg"
EOF

%files
%doc LICENSE AUTHORS
%dir %{_libdir}/calamares
%dir %{_datadir}/calamares
%dir %{_datadir}/calamares/branding
%dir %{_datadir}/calamares/branding/auto
%{_bindir}/calamares
%{_datadir}/calamares/settings.conf
%{_datadir}/calamares/branding/default/
%{_datadir}/calamares/modules/
%{_datadir}/applications/calamares.desktop
%{_datadir}/polkit-1/actions/com.github.calamares.calamares.policy
%{_sysconfdir}/calamares/
%{_libdir}/calamares/*
%ghost %{_datadir}/calamares/branding/auto/branding.desc

%files -n %{libname}
%{_libdir}/libcalamares.so.%{major}*
%{_libdir}/libcalamaresui.so.%{major}*
# unversioned library
%{_libdir}/libcalapm.so

%files -n %{develname}
%dir %{_includedir}/libcalamares
%dir %{_libdir}/cmake/Calamares
%{_includedir}/libcalamares/*
%{_libdir}/libcalamares.so
%{_libdir}/libcalamaresui.so
%{_libdir}/cmake/Calamares/*
