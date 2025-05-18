#
# spec file for package duckdb
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           duckdb
Version:        1.2.1
Release:        0
Summary:        DuckDB is an analytical in-process SQL database management system
License:        MIT
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make
BuildRequires:  ninja
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  pkgconfig(libssl)

%description
DuckDB is a high-performance analytical database system.

DuckDB provides a rich SQL dialect, with support far beyond basic SQL.
DuckDB supports arbitrary and nested correlated subqueries, window functions,
collations, complex types (arrays, structs, maps), and several extensions
designed to make SQL easier to use.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
DuckDB is a high-performance analytical database system.

This package contains the development files for %{name}.

%package -n libduckdb
Summary:        DuckDB shared library

%description -n libduckdb
DuckDB is a high-performance analytical database system.

This package contains the shared library for %{name}.

%prep
%autosetup -p1

%build
%define __builder ninja

%cmake \
    -DBUILD_UNITTESTS=OFF \
    -DEXTENSION_STATIC_BUILD=ON \
    -DOVERRIDE_GIT_DESCRIBE=v%{version}

%cmake_build

%install
%cmake_install

find %{buildroot}%{_libdir} -name '*.a' -delete

%files
%license LICENSE
%doc README.md
%{_bindir}/duckdb

%files devel
%{_includedir}/duckdb*
%{_libdir}/cmake/DuckDB/

%files -n libduckdb
%{_libdir}/libduckdb.so

%changelog
