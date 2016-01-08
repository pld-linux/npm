# TODO
# - put man3 to some -devel-doc package (man pages for npm programming)
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
Summary:	A package manager for node.js
Name:		npm
Version:	1.4.10
Release:	1
License:	Artistic-2.0
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	e2f71d8cbed5711ac46a2a9ede601690
Patch0:		link-globalPaths.patch
Patch1:		cmd-shim-optional.patch
URL:		http://npmjs.org/
BuildRequires:	bash
BuildRequires:	nodejs >= 0.9
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs
Requires:	nodejs-abbrev < 1.1.0
Requires:	nodejs-abbrev >= 1.0.4
Requires:	nodejs-ansi < 0.3.0
Requires:	nodejs-ansi >= 0.2.1
Requires:	nodejs-ansicolors < 0.4.0
Requires:	nodejs-ansicolors >= 0.3.2
Requires:	nodejs-ansistyles < 0.2.0
Requires:	nodejs-ansistyles >= 0.1.3
Requires:	nodejs-archy < 1.0.0
Requires:	nodejs-block-stream = 0.0.7
Requires:	nodejs-child-process-close < 0.2.0
Requires:	nodejs-child-process-close >= 0.1.1
Requires:	nodejs-chmodr < 0.2.0
Requires:	nodejs-chmodr >= 0.1.0
Requires:	nodejs-chownr < 1.0.0
Requires:	nodejs-columnify = 0.1.2
Requires:	nodejs-devel
Requires:	nodejs-editor = 0.0.5
Requires:	nodejs-fstream < 0.2.0
Requires:	nodejs-fstream >= 0.1.25
Requires:	nodejs-fstream-npm < 0.2.0
Requires:	nodejs-fstream-npm >= 0.1.6
Requires:	nodejs-github-url-from-git = 1.1.1
Requires:	nodejs-github-url-from-username-repo < 0.2.0
Requires:	nodejs-github-url-from-username-repo >= 0.1.0
Requires:	nodejs-glob >= 3.2.9
Requires:	nodejs-graceful-fs < 3.0.0
Requires:	nodejs-graceful-fs >= 2.0.2
Requires:	nodejs-gyp < 0.14.0
Requires:	nodejs-gyp >= 0.13.0
Requires:	nodejs-ini < 1.2.0
Requires:	nodejs-ini >= 1.1.0
Requires:	nodejs-init-package-json = 0.0.16
Requires:	nodejs-lockfile < 0.5.0
Requires:	nodejs-lockfile >= 0.4.0
Requires:	nodejs-lru-cache < 2.6.0
Requires:	nodejs-lru-cache >= 2.5.0
Requires:	nodejs-minimatch < 0.3.0
Requires:	nodejs-minimatch >= 0.2.14
Requires:	nodejs-mkdirp < 0.4.0
Requires:	nodejs-mkdirp >= 0.3.5
Requires:	nodejs-nopt < 3.0.0
Requires:	nodejs-nopt >= 2.2.1
Requires:	nodejs-npm-install-checks < 1.1.0
Requires:	nodejs-npm-install-checks >= 1.0.0
Requires:	nodejs-npm-registry-client < 0.5.0
Requires:	nodejs-npm-registry-client >= 0.4.8
Requires:	nodejs-npm-user-validate = 0.0.3
Requires:	nodejs-npmconf < 0.2.0
Requires:	nodejs-npmconf >= 0.1.15
Requires:	nodejs-npmlog = 0.0.6
Requires:	nodejs-once < 1.4.0
Requires:	nodejs-once >= 1.3.0
Requires:	nodejs-opener < 1.4.0
Requires:	nodejs-opener >= 1.3.0
Requires:	nodejs-osenv < 1.0.0
Requires:	nodejs-path-is-inside < 1.1.0
Requires:	nodejs-path-is-inside >= 1.0.0
Requires:	nodejs-read < 1.1.0
Requires:	nodejs-read >= 1.0.4
Requires:	nodejs-read-installed < 2.1.0
Requires:	nodejs-read-installed >= 2.0.1
Requires:	nodejs-read-package-json < 1.2.0
Requires:	nodejs-read-package-json >= 1.1.9
Requires:	nodejs-request < 2.31.0
Requires:	nodejs-request >= 2.30.0
Requires:	nodejs-retry < 0.7.0
Requires:	nodejs-retry >= 0.6.0
Requires:	nodejs-rimraf < 2.3.0
Requires:	nodejs-rimraf >= 2.2.5
Requires:	nodejs-semver < 2.3.0
Requires:	nodejs-semver >= 2.2.1
Requires:	nodejs-sha < 1.3.0
Requires:	nodejs-sha >= 1.2.1
Requires:	nodejs-slide < 1.2.0
Requires:	nodejs-slide >= 1.1.5
Requires:	nodejs-sorted-object < 1.1.0
Requires:	nodejs-sorted-object >= 1.0.0
Requires:	nodejs-tar < 0.2.0
Requires:	nodejs-tar >= 0.1.19
Requires:	nodejs-text-table < 0.3.0
Requires:	nodejs-text-table >= 0.2.0
Requires:	nodejs-uid-number = 0.0.5
Requires:	nodejs-which < 2.0.0
Requires:	nodejs-which >= 1.0.0
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
%patch0 -p1
%patch1 -p1

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/npm-cli.js \
	cli.js

# startup helpers we don't need
rm bin/npm bin/npm.cmd

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
%doc AUTHORS LICENSE README.md
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
%{nodejs_libdir}/npm/doc/api
%{nodejs_libdir}/npm/doc/cli
%{nodejs_libdir}/npm/doc/files
%{nodejs_libdir}/npm/doc/misc

%{_mandir}/man1/npm*
%{_mandir}/man3/npm*
%{_mandir}/man5/npm*
%{_mandir}/man5/package.json.5*
%{_mandir}/man7/npm*
%{_mandir}/man7/removing-npm.7*
%{_mandir}/man7/semver.7*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
