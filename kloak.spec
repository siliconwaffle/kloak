%global commit 9cbdf4484da19eb09653356e59ce42c37cecb523
%global date 20230925
%{?commit:%global short_commit %(c=%{commit}; echo ${c:0:7})}

Name:           kloak
Version:        0.2^%{date}g%{short_commit}
Release:        %autorelease
Summary:        Keystroke-level online anonymization kernel

License:        BSD-3-Clause
URL:            https://github.com/vmonaco/%{name}
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}

%description
A privacy tool that makes keystroke biometrics less effective. This is
accomplished by obfuscating the time intervals between key press and release
events, which are typically used for identification.

%prep
%autosetup -n %{name}-%{commit}

%build
%make_build all

%install
%__install -Dm 644 lib/systemd/system/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%__install -Dm 755 eventcap %{buildroot}%{_sbindir}/eventcap
%__install -Dm 755 %{name} %{buildroot}%{_sbindir}/%{name}
%__install -Dm 644 auto-generated-man-pages/eventcap.8 %{buildroot}%{_mandir}/man8/eventcap.8
%__install -Dm 644 auto-generated-man-pages/%{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%{_unitdir}/%{name}.service
%{_sbindir}/eventcap
%{_sbindir}/%{name}
%{_mandir}/man8/eventcap.8*
%{_mandir}/man8/%{name}.8*

%changelog
* Mon Jul 29 2024 Jonathon Hyde <siliconwaffle@trilbyproject.org> - 0.2^20230925g9cbdf44-1
- Initial RPM Release
