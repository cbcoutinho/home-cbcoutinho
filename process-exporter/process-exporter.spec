#
# spec file for package process-exporter
#
# Copyright (c) 2026 SUSE LLC
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


Name:           process-exporter
Version:        0.8.5
Release:        0
Summary:        Prometheus exporter for process metrics
License:        MIT
URL:            https://github.com/ncabatoff/process-exporter
Source0:        %{name}-%{version}.tar.gz
Source1:        vendor.tar.zst
Source100:      %{name}-rpmlintrc
BuildRequires:  golang(API) >= 1.23
BuildRequires:  systemd-rpm-macros
BuildRequires:  zstd
%{?systemd_ordering}

%description
process-exporter mines information about running processes from /proc and
exports it to Prometheus. Processes are grouped by a user-supplied naming
scheme, and metrics such as CPU time, memory usage, I/O, file descriptor
counts and context switches are reported per group.

%prep
%autosetup -p1 -a1

%build
export CGO_ENABLED=0
export GOFLAGS="-mod=vendor"
# Reproducible build stamp: prefer SOURCE_DATE_EPOCH when rpm provides it.
build_date=$(date -u -d "@${SOURCE_DATE_EPOCH:-$(date +%%s)}" +%%Y%%m%%d-%%H:%%M:%%S)
go build \
    -buildmode=pie \
    -ldflags "-X main.version=%{version} \
              -X github.com/prometheus/common/version.Version=%{version} \
              -X github.com/prometheus/common/version.Revision=v%{version} \
              -X github.com/prometheus/common/version.Branch=master \
              -X github.com/prometheus/common/version.BuildUser=obs@build.opensuse.org \
              -X github.com/prometheus/common/version.BuildDate=${build_date}" \
    -o %{name} \
    ./cmd/process-exporter

%install
install -D -m0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m0644 packaging/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m0644 packaging/conf/all.yaml %{buildroot}%{_sysconfdir}/%{name}/all.yaml
install -D -m0644 packaging/default/%{name} %{buildroot}%{_sysconfdir}/default/%{name}
mkdir -p %{buildroot}%{_sbindir}
ln -s service %{buildroot}%{_sbindir}/rc%{name}

%pre
%service_add_pre %{name}.service

%post
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_sbindir}/rc%{name}
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/all.yaml
%config(noreplace) %{_sysconfdir}/default/%{name}

%changelog
