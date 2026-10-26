%ifarch aarch64
    %global _lto_cflags %nil
%endif

%global appname AyuGramDesktop

# Reduce debuginfo size
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

Name:    ayugram-desktop
Version: 7.2.9
Release: 1%{?dist}

License: GPL-3.0-or-later AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain AND LGPL-2.1-or-later AND FTL AND MPL-1.1 AND OFL-1.1 AND Unicode-3.0
URL:     https://github.com/AyuGram/%{appname}
Summary: Desktop Telegram client with good customization and Ghost mode
Source0: %{url}/releases/download/v%{version}/%{appname}-%{version}-full.tar.gz

# cld3: fall back to FindProtobuf when protobuf CMake config is absent
Patch0:  findprotobuf_fix.patch

# Linking needs >8 GB RAM
ExclusiveArch: aarch64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6GuiPrivate)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6WidgetsPrivate)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(ada)
BuildRequires: cmake(fmt)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tde2e)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.68) >= 2.76.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(openh264)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(webkitgtk-6.0)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libdispatch-devel
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3

Requires: hicolor-icon-theme
Requires: qt6-qtimageformats%{?_isa}
Requires: webkitgtk6.0%{?_isa}

Provides: ayugram = %{version}-%{release}
Provides: ayugram%{?_isa} = %{version}-%{release}

%description
AyuGram is a Telegram Desktop fork with ghost mode, message history,
anti-recall and extended customization.

Unofficial build, not affiliated with Radolyn Labs.

%prep
%autosetup -n %{appname}-%{version}-full -p1

# Unbundle everything available in Fedora except minizip
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx5-qt,hime,hunspell,kimageformats,lz4,nimf,range-v3,xxHash}

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_ID=2040 \
    -DTDESKTOP_API_HASH=b18441a1ff607e10a989891a5462e627 \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_QT_PLUGINS:BOOL=ON
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.ayugram.desktop.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/com.ayugram.desktop.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/AyuGram
%{_datadir}/applications/com.ayugram.desktop.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/dbus-1/services/com.ayugram.desktop.service
%{_metainfodir}/com.ayugram.desktop.metainfo.xml

%changelog
* Mon Oct 26 2026 Eugene <e.rusalev@gmail.com> - 7.2.9-1
- Initial COPR packaging, based on RPM Fusion spec by Ivan Romanov
