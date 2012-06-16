# TODO
# - put man3 to some -devel-doc package (man pages for npm programming)
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
Summary:	A package manager for node.js
Name:		npm
Version:	1.1.19
Release:	2
License:	MIT License
Group:		Development/Libraries
URL:		http://npmjs.org/
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	1838db326e36430b7cf78f0c5aa77636
BuildRequires:	bash
BuildRequires:	nodejs >= 0.6
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs
Requires:	nodejs-abbrev >= 1.0.3
Requires:	nodejs-archy
Requires:	nodejs-block-stream >= 0.0.5
Requires:	nodejs-chownr
Requires:	nodejs-devel
Requires:	nodejs-fast-list
Requires:	nodejs-fstream >= 0.1.17
Requires:	nodejs-fstream-npm
Requires:	nodejs-graceful-fs >= 1.1.8
Requires:	nodejs-inherits
Requires:	nodejs-ini >= 1.0.1
Requires:	nodejs-lru-cache >= 1.0.6
Requires:	nodejs-minimatch >= 0.2.2
Requires:	nodejs-mkdirp
Requires:	nodejs-node-uuid >= 1.3.3
Requires:	nodejs-nopt
Requires:	nodejs-proto-list
Requires:	nodejs-read
Requires:	nodejs-request >= 2.9.153
Requires:	nodejs-rimraf >= 1.0.9
Requires:	nodejs-semver >= 1.0.13
Requires:	nodejs-slide-flow-control
Requires:	nodejs-tar >= 0.1.13
Requires:	nodejs-uid-number
Requires:	nodejs-which
# gyp used for binary packages in nodejs
Suggests:	nodejs-gyp >= 0.3.8
# waf used for binary packages in nodejs < 0.8
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

%build
# forces npm to keep config files in /etc instead of /usr/etc
./configure \
	--globalconfig=%{_sysconfdir}/npmrc \
	--globalignorefile=%{_sysconfdir}/npmignore

cat npmrc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/npm/bin,/etc/bash_completion.d}
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/npm/bin

cp -a lib cli.js npmrc package.json $RPM_BUILD_ROOT%{nodejs_libdir}/npm
cp -p bin/*.js $RPM_BUILD_ROOT%{nodejs_libdir}/npm/bin
ln -s %{nodejs_libdir}/npm/bin/npm-cli.js $RPM_BUILD_ROOT%{_bindir}/npm

# for npm help
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc
cp -a doc/* $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc

# ghosted global config files
# TODO: package as files to have file permissions set
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p npmrc $RPM_BUILD_ROOT%{_sysconfdir}/npmrc
touch $RPM_BUILD_ROOT%{_sysconfdir}/npmignore

# install to mandir
install -d $RPM_BUILD_ROOT%{_mandir}
cp -pr man/* $RPM_BUILD_ROOT%{_mandir}

# FIXME: "npm help" requires this
ln -s %{_mandir} $RPM_BUILD_ROOT%{nodejs_libdir}/npm/man

mv $RPM_BUILD_ROOT%{nodejs_libdir}/npm/lib/utils/completion.sh \
	$RPM_BUILD_ROOT/etc/bash_completion.d/%{name}.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md doc/cli/changelog.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%attr(755,root,root) %{_bindir}/npm
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/package.json
%{nodejs_libdir}/npm/cli.js
%{nodejs_libdir}/npm/npmrc

%dir %{nodejs_libdir}/npm/bin
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-cli.js
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

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
