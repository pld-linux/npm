# TODO
# - put man3 to some -devel-doc package (man pages for npm programming)
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead

# build package without bundled node-gyp module
%bcond_without  bundled_gyp 

Summary:	A package manager for node.js
Name:		npm
Version:	3.10.8
Release:	1
License:	Artistic-2.0
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	f470ec0065a5a181a432f008a3a97dda
Patch0:		link-globalPaths.patch 
Patch1:		cmd-shim-optional.patch
URL:		http://npmjs.org/
BuildRequires:	bash
BuildRequires:	nodejs >= 0.9
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs
%if %{without bundled_gyp}
Suggests:	nodejs-gyp
Conflicts:	nodejs-gyp < 3.5.0
Conflicts:	nodejs-gyp >= 3.4.0
%endif
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

# clean up node_modules/
for i in README.md Readme.md README.markdown LICENSE LICENSE.md CHANGES.md \
         changelog.md .npmignore .travis.yml test examples example; do 
	find node_modules -name $i | xargs -r rm -r
done
rm lib/fetch-package-metadata.md

%if %{without bundled_gyp}
rm -r node_modules/node-gyp
%endif
cp -r node_modules $RPM_BUILD_ROOT%{nodejs_libdir}/npm/

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
%{nodejs_libdir}/npm/lib/cache
%{nodejs_libdir}/npm/lib/config
%{nodejs_libdir}/npm/lib/install
%{nodejs_libdir}/npm/lib/utils
%{nodejs_libdir}/npm/node_modules

# man symlink
%{nodejs_libdir}/npm/man

%dir %{nodejs_libdir}/npm/doc
%{nodejs_libdir}/npm/doc/cli
%{nodejs_libdir}/npm/doc/files
%{nodejs_libdir}/npm/doc/misc

%{_mandir}/man1/npm*
%{_mandir}/man5/npm*
%{_mandir}/man5/package.json.5*
%{_mandir}/man7/npm*
%{_mandir}/man7/removing-npm.7*
%{_mandir}/man7/semver.7*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
