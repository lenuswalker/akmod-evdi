Name:           akmod-evdi
Version:        1.14.10
Release:        2%{?dist}
Summary:        Akmods wrapper for EVDI (ships evdi-kmod SRPM for akmods to rebuild)
License:        GPL-2.0-only AND MIT
URL:            https://github.com/DisplayLink/evdi
Source0:        https://github.com/DisplayLink/evdi/archive/refs/tags/v%{version}.tar.gz#/evdi-%{version}.tar.gz

BuildArch:      noarch
%global debug_package %{nil}
%undefine _package_debug
%undefine _build_id_links
%undefine _missing_build_ids_terminate_build
%undefine _debuginfo
%undefine _debugsource_packages

BuildRequires:  rpm-build
BuildRequires:  kmodtool
BuildRequires:  redhat-rpm-config
BuildRequires:  gcc, make
Requires:       akmods

%description
This package provides the kmod SRPM (evdi-kmod) for the EVDI kernel module.
akmods will rebuild and install the binary kmod for the running kernel as needed.

%prep
# nothing to unpack here; we'll build the kmod SRPM from the upstream tarball

%build
# Create a temporary build area for generating the kmod SRPM
mkdir -p %{_builddir}/evdi-kmod-src/{SOURCES,SPECS}
cp -p %{SOURCE0} %{_builddir}/evdi-kmod-src/SOURCES/evdi-%{version}.tar.gz

# Generate a minimal kmod spec using kmodtool (RPM Fusion style)
cat > %{_builddir}/evdi-kmod-src/SPECS/evdi-kmod.spec <<'SPEC'
%define kmod_name evdi
%define kmod_version %{version}
%define kmod_release %{release}

%define kmodtool /usr/bin/kmodtool
%{!?kmodtool: %define kmodtool /usr/bin/kmodtool}

%define kverrel %{nil}
%define kvariants %{nil}

Name:           %{kmod_name}-kmod
Version:        %{kmod_version}
Release:        %{kmod_release}
Summary:        %{kmod_name} kernel module
Group:          System Environment/Kernel
License:        GPLv2 and MIT
URL:            https://github.com/DisplayLink/evdi
Source0:        evdi-%{version}.tar.gz
BuildRequires:  gcc, make, elfutils-libelf-devel
# akmods will inject kernel-devel at build time for the target kernel

%description
EVDI kernel module built as a kmod package.

%prep
%setup -q -n evdi-%{version}

%build
# nothing to build at SRPM time

%install
# nothing to install at SRPM time

%files
# no files in the SRPM

%changelog
* Sun Aug 24 2025 Lenus Walker <lenusiwalker@outlook.com> - %{kmod_version}-%{kmod_release}
- Initial evdi-kmod SRPM for akmods consumption
SPEC

# Build the SRPM (no binary build now)
rpmbuild -bs --nodeps --define "_sourcedir %{_builddir}/evdi-kmod-src/SOURCES" \
                  --define "_specdir   %{_builddir}/evdi-kmod-src/SPECS" \
                  --define "_srcrpmdir %{_builddir}" \
                  %{_builddir}/evdi-kmod-src/SPECS/evdi-kmod.spec

%install
# Install the generated SRPM to /usr/src/akmods and add a helpful symlink
install -d %{buildroot}/usr/src/akmods
install -m0644 %{_builddir}/evdi-kmod-%{version}-%{release}.src.rpm \
        %{buildroot}/usr/src/akmods/evdi-kmod-%{version}-%{release}.src.rpm
ln -s evdi-kmod-%{version}-%{release}.src.rpm \
      %{buildroot}/usr/src/akmods/evdi-kmod.src.rpm

%files
/usr/src/akmods/evdi-kmod-%{version}-%{release}.src.rpm
/usr/src/akmods/evdi-kmod.src.rpm

%changelog
* Sun Aug 24 2025 Lenus Walker <lenusiwalker@outlook.com> - 1.14.10-2
- Ship evdi-kmod SRPM under /usr/src/akmods so akmods can find and rebuild it
