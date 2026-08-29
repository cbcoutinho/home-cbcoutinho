#
# spec file for package gcx
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


Name:           gcx
Version:        1.2.0
Release:        0
Summary:        Command line interface for Grafana
License:        Apache-2.0
URL:            https://github.com/grafana/gcx
Source0:        %{name}-%{version}.tar.gz
Source1:        vendor.tar.zst
Source100:      %{name}-rpmlintrc
BuildRequires:  golang(API) >= 1.26
BuildRequires:  zstd

%description
gcx is a command line interface for Grafana Cloud, Enterprise and OSS
(Grafana 12+). It gives structured access to dashboards, alerts, SLOs,
metrics, logs and traces, and ships agent skills for workflows such as alert
investigation, dashboard creation and GitOps, SLO management and
observability setup.

%prep
%autosetup -p1 -a1

%build
export CGO_ENABLED=0
export GOFLAGS="-mod=vendor"
# Reproducible build stamp: prefer SOURCE_DATE_EPOCH when rpm provides it.
build_date=$(date -u -d "@${SOURCE_DATE_EPOCH:-$(date +%%s)}" +%%Y-%%m-%%dT%%H:%%M:%%SZ)
go build \
    -buildmode=pie \
    -trimpath \
    -ldflags "-X main.version=%{version} \
              -X main.commit=v%{version} \
              -X main.date=${build_date}" \
    -o %{name} \
    ./cmd/%{name}

%install
install -D -m0755 %{name} %{buildroot}%{_bindir}/%{name}

# Cobra generates the shell completions from the built binary. Keep it away
# from any real config and telemetry endpoint while doing so.
export GCX_TELEMETRY=disabled
export HOME=%{_builddir}
./%{name} completion bash > %{name}.bash
./%{name} completion zsh > %{name}.zsh
./%{name} completion fish > %{name}.fish
install -D -m0644 %{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -D -m0644 %{name}.zsh %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -D -m0644 %{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%changelog
