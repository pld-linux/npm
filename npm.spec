# TODO
# - put man3 to some -devel-doc package (man pages for npm programming)
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
# - package new node deps
# - global config seems wrong:
# $ npm config get globalconfig
# /usr/etc/npmrc
Summary:	A package manager for node.js
Name:		npm
Version:	1.1.18
Release:	0.1
License:	MIT License
Group:		Development/Libraries
URL:		http://npmjs.org/
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	eb1303e3208dfd6cf2dc663b6caca381
BuildRequires:	nodejs >= 0.4
BuildRequires:	rpmbuild(macros) >= 1.634
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
# waf used for binary packages
Suggests:	nodejs-waf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NPM is a package manager for node.js. You can use it to install and
publish your node programs. It manages dependencies and does other
cool stuff.

%package -n bash-completion-%{name}
Summary:	bash-completion for %{name}
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla %{name}
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion

%description -n bash-completion-%{name}
bash-completion for %{name}.

%description -n bash-completion-%{name} -l pl.UTF-8
bashowe uzupełnianie nazw dla %{name}.

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/npm,/etc/bash_completion.d}

cp -a bin lib node_modules package.json *.js $RPM_BUILD_ROOT%{nodejs_libdir}/npm
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

mv $RPM_BUILD_ROOT%{nodejs_libdir}/npm/lib/utils/completion.sh \
	$RPM_BUILD_ROOT/etc/bash_completion.d/%{name}.sh

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
%attr(755,root,root) %{_bindir}/npm
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/*.js
%{nodejs_libdir}/npm/package.json

%dir %{nodejs_libdir}/npm/bin
%attr(755,root,root) %{nodejs_libdir}/npm/bin/*.js
%dir %{nodejs_libdir}/npm/bin/node-gyp-bin/
%attr(755,root,root) %{nodejs_libdir}/npm/bin/node-gyp-bin/node-gyp
%dir %{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/lib/*.js
%{nodejs_libdir}/npm/lib/utils
%{nodejs_libdir}/npm/node_modules

# man symlink
%{nodejs_libdir}/npm/man

%dir %{nodejs_libdir}/npm/doc
%{nodejs_libdir}/npm/doc/cli
%{nodejs_libdir}/npm/doc/api

%{_mandir}/man1/npm*
%{_mandir}/man3/npm*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
