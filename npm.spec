# TODO
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
Summary:	A package manager for node.js
Name:		npm
Version:    1.1.0
Release:	0.9
License:	MIT License
Group:		Development/Libraries
URL:		http://npmjs.org/
Source0:    http://registry.npmjs.org/npm/-/npm-%{version}-2.tgz
# Source0-md5:	f3beb0775b52ac3235f814b59efc5824
BuildRequires:	nodejs >= 0.4
Requires:	nodejs
Requires:	nodejs-abbrev >= 1.0.3
Requires:	nodejs-block-stream
Requires:	nodejs-fast-list
Requires:	nodejs-fstream
Requires:	nodejs-graceful-fs >= 1.1.4
Requires:	nodejs-inherits
Requires:	nodejs-ini
Requires:	nodejs-minimatch
Requires:	nodejs-mkdirp
Requires:	nodejs-node-uuid >= 1.3.3
Requires:	nodejs-nopt
Requires:	nodejs-proto-list
Requires:	nodejs-read
Requires:	nodejs-request >= 2.9.100
Requires:	nodejs-rimraf >= 1.0.9
Requires:	nodejs-semver >= 1.0.13
Requires:	nodejs-slide-flow-control
Requires:	nodejs-tar
Requires:	nodejs-which
Suggests:	nodejs-devel
Suggests:	nodejs-waf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		nodejs_libdir %{_prefix}/lib/node_modules

%description
NPM is a package manager for node.js. You can use it to install and
publish your node programs. It manages dependencies and does other
cool stuff.

%prep
%setup -qc
mv package/* .

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/npm-cli.js \
	cli.js \
	lib/utils/cmd-shim.js \

# startup helpers we don't need
rm bin/npm bin/npm.cmd

# prefix all manpages with "npm-"
for dir in man/man*; do
    cd $dir
    for page in *; do
        if [[ $page != npm* ]]; then
            mv $page npm-$page
        fi
    done
    cd -
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/npm}

cp -a bin lib package.json $RPM_BUILD_ROOT%{nodejs_libdir}/npm
ln -s %{nodejs_libdir}/npm/bin/npm-cli.js $RPM_BUILD_ROOT%{_bindir}/npm

# for npm help
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc
cp -a doc/* $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc

# ghosted global config files
# TODO: package as files to have file permissions set
install -d $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/npmrc
touch $RPM_BUILD_ROOT%{_sysconfdir}/npmignore

# install to mandir
install -d $RPM_BUILD_ROOT%{_mandir}
cp -pr man/* $RPM_BUILD_ROOT%{_mandir}

# FIXME: "npm help" requires this
ln -s %{_mandir} $RPM_BUILD_ROOT%{nodejs_libdir}/npm/man

# TODO bash-completion separate package
rm $RPM_BUILD_ROOT%{nodejs_libdir}/npm/lib/utils/completion.sh

%if 0
%post
# This section is the workaround does not work properly npm install.
%{_bindir}/npm config set registry http://registry.npmjs.org/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md doc/cli/changelog.md
%ghost %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%attr(755,root,root) %{_bindir}/npm*
# TODO: top dir to nodejs package
%dir %{nodejs_libdir}
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/package.json

%dir %{nodejs_libdir}/npm/bin
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-cli.js
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-get-uid-gid.js
%attr(755,root,root) %{nodejs_libdir}/npm/bin/read-package-json.js
%dir %{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/lib/*.js
%{nodejs_libdir}/npm/lib/utils

# man symlink
%{nodejs_libdir}/npm/man

%dir %{nodejs_libdir}/npm/doc
%{nodejs_libdir}/npm/doc/cli
%{nodejs_libdir}/npm/doc/api

%{_mandir}/man1/npm*
%{_mandir}/man3/npm*
