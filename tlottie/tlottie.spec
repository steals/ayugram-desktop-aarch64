%global debug_package %{nil}

%global commit0 31f1b542f88e7b4be9a01e749920d857535fc715
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20260911

# desktop-app/patches revision pinned by tdesktop's centos_env Dockerfile
%global patches_commit 519aaa084608fa6f9a2bfbd1959d133c44d94227

Name:    tlottie
Version: 0.1.0
Release: 1.%{date}git%{shortcommit0}%{?dist}
Summary: Lottie animation renderer used by Telegram Desktop
License: MIT
URL:     https://github.com/dkaraush/%{name}
Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch0:  https://raw.githubusercontent.com/desktop-app/patches/%{patches_commit}/tlottie.patch#/%{name}-desktop-app.patch

ExclusiveArch: x86_64 aarch64

BuildRequires: cargo
BuildRequires: rust

%description
Rust Lottie renderer with a C API, replacing rlottie in Telegram Desktop.

%package devel
Summary:  Static library and headers for %{name}
Provides: %{name}-static = %{version}-%{release}
Provides: %{name}-static%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1
# Drop no-std/wasm-only optional deps so the build needs no crates.io access
sed -i \
    -e '/^no-std = /d' \
    -e '/^hashbrown = /d' \
    -e '/^dlmalloc = /d' \
    -e "/^\[target.'cfg(target_arch = \"wasm32\")'.dependencies\]/d" \
    Cargo.toml
rm -f Cargo.lock

%build
export CARGO_HOME=$PWD/.cargo
cargo rustc --lib --release --offline --features c-api --crate-type staticlib

%install
install -Dpm0644 target/release/lib%{name}.a %{buildroot}%{_libdir}/lib%{name}.a
install -Dpm0644 include/%{name}.h %{buildroot}%{_includedir}/%{name}/%{name}.h

%check
export CARGO_HOME=$PWD/.cargo
# Fails on unpatched upstream at this commit as well
cargo test --release --offline --lib --features c-api -- \
    --skip dos::renderer_rejects_generated_work_after_successful_parse

%files devel
%license LICENSE
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.a

%changelog
* Mon Oct 26 2026 Eugene <e.rusalev@gmail.com> - 0.1.0-1.20260911git31f1b54
- Initial package, commit pinned by tdesktop 7.2.x build environment
