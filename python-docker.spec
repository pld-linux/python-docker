#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module		docker
%define		egg_name	docker
%define		pypi_name	docker
Summary:	A Python 2 library for the Docker Engine API
Summary(pl.UTF-8):	Biblioteka Pythona 2 do API silnika Docker
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.4.4
Release:	3
Epoch:		1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/d/docker/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	e52f862b113d14c684a6e7dfa3d9e11c
Patch0:		unpin-requirements.patch
URL:		http://docker-py.readthedocs.org/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:42
%if %{with tests}
BuildRequires:	python-ipaddress >= 1.0.16
BuildRequires:	python-backports-ssl_match_hostname >= 3.5
BuildRequires:	python-pytest >= 4.3.1
BuildRequires:	python-pytest-timeout >= 1.3.3
BuildRequires:	python-requests >= 2.20.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-urllib3 >= 1.24.3
BuildRequires:	python-websocket-client >= 0.56.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildConflicts:	python-docker < 2.0
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3
# optional dep for ssh support (required by docker-compose)
Suggests:	python-paramiko >= 2.4.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%description -l pl.UTF-8
Biblioteka Pythona do API silnika Docker. Pozwala zrobić wszystko to,
co polecenie "docker", ale z poziomu aplikacji w Pythonie: uruchamiać
kontenery, zarządzać nimi, zarządzać Swarmami itp.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch -P0 -p1

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_timeout" \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests/unit -k 'not TCPSocketStreamTest'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
