Name:           akmod-evdi
Version:        1.14.10
Release:        3%{?dist}
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
BuildRequires:  redhat-rpm-config
BuildRequires:  gcc, make
Requires:       akmods

%description
This package provides the kmod SRPM (evdi-kmod) for the EVDI kernel module.
akmods will rebuild and install the binary kmod for the running kernel as needed.

%prep
# nothing to unpack here; we’ll generate the kmod SRPM spec and build it

%build
# Create temp tree for the SRPM build
mkdir -p %{_builddir}/evdi-kmod-src/{SOURCES,SPECS}
cp -p %{SOURCE0} %{_builddir}/evdi-kmod-src/SOURCES/evdi-%{version}.tar.gz

# Write a minimal kmod spec (NOTE: double % to avoid rpm parsing these as our own sections)
cat > %{_builddir}/evdi-kmod-src/SPECS/evdi-kmod.spec <<'SPEC_EOF'
%%define kmod_name evdi
%%define kmod_version %{version}
%%define kmod_release %{release}

Name:           %%{kmod_name}-kmod
Version:        %%{kmod_version}
Release:        %%{kmod_release}
Summary:        %%{kmod_name} kernel module
Group:          System Environment/Kernel
License:        GPLv2 and MIT
URL:            https://github.com/DisplayLink/evdi
Source0:        evdi-%%{version}.tar.gz
BuildRequires:  gcc, make, elfutils-libelf-devel

%%description
EVDI kernel module built as a kmod package.

%%prep
%%setup -q -n evdi-%%{version}

%%build
# Binary build happens when akmods rebuilds for a specific kernel.

%%install
# Nothing to install in SRPM build.

%%files
# SRPM only; no files here.

%%changelog
* Sun Aug 24 2025 Lenus Walker <lenusiwalker@outlook.com> - %%{kmod_version}-%%{kmod_release}
- Initial evdi-kmod SRPM for akmods consumption
SPEC_EOF

# Build the SRPM (no binary build here)
rpmbuild -bs --nodeps \
  --define "_sourcedir %{_builddir}/evdi-kmod-src/SOURCES" \
  --define "_specdir   %{_builddir}/evdi-kmod-src/SPECS" \
  --define "_srcrpmdir %{_builddir}" \
  %{_builddir}/evdi-kmod-src/SPECS/evdi-kmod.spec

%install
install -d %{buildroot}/usr/src/akmods
install -m0644 %{_builddir}/evdi-kmod-%{version}-%{release}.src.rpm \
        %{buildroot}/usr/src/akmods/evdi-kmod-%{version}-%{release}.src.rpm
ln -s evdi-kmod-%{version}-%{release}.src.rpm \
      %{buildroot}/usr/src/akmods/evdi-kmod.src.rpm

%files
/usr/src/akmods/evdi-kmod-%{version}-%{release}.src.rpm
/usr/src/akmods/evdi-kmod.src.rpm

%changelog
* Sun Aug 24 2025 Lenus Walker <lenusiwalker@outlook.com> - 1.14.10-3
- Escape inner spec section headers (%%) to fix “second Description/second prep” parse errors
