# TODO
# - rather quickly thrown together, install methology could change later
# - man fixes: npm ERR! Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
Summary:	A package manager for Node.js
Name:		npm
Version:	1.0.106
Release:	0.4
License:	MIT License
Group:		Development/Libraries
URL:		http://npmjs.org/
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	44f82461713f911d9a01f194bdc891bd
BuildRequires:	nodejs >= 0.4
Requires:	nodejs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME: to to match files section this has this value now
# TODO: this needs to be %{_libdir}/node
%define		nodejs_libdir %{_prefix}/lib/node_modules

%description
NPM is a package manager for Node.js. You can use it to install and
publish your node programs. It manages dependencies and does other
cool stuff.

%prep
%setup -qc
mv package/* .

%build
./configure \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	root=$RPM_BUILD_ROOT%{_prefix}/lib/node \
	binroot=$RPM_BUILD_ROOT%{_bindir} \
	manroot=$RPM_BUILD_ROOT%{_mandir} \

%install
rm -rf $RPM_BUILD_ROOT

node cli.js install -global

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	$RPM_BUILD_ROOT%{nodejs_libdir}/npm/bin/*.js \
	$RPM_BUILD_ROOT%{nodejs_libdir}/npm/cli.js \
	$RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/semver/bin/semver \
	$RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/which/bin/which \
	$RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/nopt/bin/nopt.js

# move symlinks to be files
find $RPM_BUILD_ROOT%{_mandir} -type l | while read man; do
	src=$(readlink -f $man)
	rm $man
	mv $src $man
done

# we keep only man format
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc/api
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc/cli
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/html/doc
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/html/api
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/html

# not everything copied is useful
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/test
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/npmrc
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/package
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/scripts
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/AUTHORS
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/CHANGES
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/LICENSE
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/Makefile
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/README.md
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/deps/basic-bsdtar-*
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/.bin
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/configure

rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/request/tests
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/ini/test
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/minimatch/test
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/node-uuid/test
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/rimraf/test
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/semver/test.js

# TODO: package examples to %{_prefix}/src
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/node_modules/nopt/examples

# TODO bash-completion separate package
rm -rf $RPM_BUILD_ROOT%{nodejs_libdir}/npm/lib/utils/completion.sh

%if 0
%post
# This section is the workaround does not work properly npm install.
%{_bindir}/npm config set registry http://registry.npmjs.org/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE README.md
%attr(755,root,root) %{_bindir}/npm*
%dir %{nodejs_libdir}
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/package.json

%dir %{nodejs_libdir}/npm/bin
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-cli.js
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-get-uid-gid.js
%attr(755,root,root) %{nodejs_libdir}/npm/bin/read-package-json.js
%{nodejs_libdir}/npm/cli.js
%dir %{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/lib/*.js
%{nodejs_libdir}/npm/lib/utils

# npm private modules: TODO: use external pkgs
%dir %{nodejs_libdir}/npm/node_modules
%{nodejs_libdir}/npm/node_modules/abbrev
%{nodejs_libdir}/npm/node_modules/graceful-fs
%{nodejs_libdir}/npm/node_modules/ini
%{nodejs_libdir}/npm/node_modules/minimatch
%{nodejs_libdir}/npm/node_modules/node-uuid
%{nodejs_libdir}/npm/node_modules/nopt
%{nodejs_libdir}/npm/node_modules/proto-list
%{nodejs_libdir}/npm/node_modules/request
%{nodejs_libdir}/npm/node_modules/rimraf
%{nodejs_libdir}/npm/node_modules/semver
%{nodejs_libdir}/npm/node_modules/slide
%{nodejs_libdir}/npm/node_modules/which

%{_mandir}/man1/npm*
%{_mandir}/man3/npm*
