Name:           akmod-evdi
Version:        1.14.10
Release:        1%{?dist}
Summary:        Akmods package for the EVDI (DisplayLink) kernel module
License:        GPL-2.0-only AND MIT
URL:            https://github.com/DisplayLink/evdi
Source0:        https://github.com/DisplayLink/evdi/archive/refs/tags/v%{version}.tar.gz#/evdi-%{version}.tar.gz

BuildRequires:  akmods
BuildRequires:  gcc, make
Requires:       akmods
Requires:       kernel-devel-uname-r >= 0
Provides:       kmod(evdi)

%description
EVDI kernel module built by akmods at boot/update time on Fedora Atomic systems.

%prep
%autosetup -n evdi-%{version}

%build
# akmods compiles on target; nothing to build here.

%install
mkdir -p %{buildroot}/usr/src/akmods/evdi-%{version}
cp -a * %{buildroot}/usr/src/akmods/evdi-%{version}/

# Minimal akmods metadata
cat > %{buildroot}/usr/src/akmods/evdi-%{version}/akmod.xml <<'XML'
<akmod>
  <kmod name="evdi" />
</akmod>
XML

# Build helper used by akmods on target
cat > %{buildroot}/usr/src/akmods/evdi-%{version}/kmodtool-extra.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
KERNELDIR="$1"
make -C "$KERNELDIR" M="$PWD/module" modules
install -D -m 0644 module/evdi.ko "$PWD"/result/evdi.ko
SH
chmod +x %{buildroot}/usr/src/akmods/evdi-%{version}/kmodtool-extra.sh

%files
/usr/src/akmods/evdi-%{version}
