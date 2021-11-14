# TODO
# - put man3 to some -devel-doc package (man pages for npm programming)
# - it can't live without this path: Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
#
# Conditional build:
%bcond_without  bundled_gyp	# package without bundled node-gyp module

Summary:	A package manager for node.js
Summary(pl.UTF-8):	Zarządca pakietów dla node.js
Name:		npm
Version:	6.14.15
Release:	2
License:	Artistic v2.0
Group:		Development/Tools
Source0:	https://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	51bb7ac69421253bdf08c7a09b7966bc
Patch0:		link-globalPaths.patch
Patch1:		cmd-shim-optional.patch
URL:		https://www.npmjs.com/
BuildRequires:	bash
BuildRequires:	nodejs >= 6
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs >= 6
%if %{without bundled_gyp}
Suggests:	nodejs-gyp = 5.1.0
Conflicts:	nodejs-gyp < 5.1.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NPM is a package manager for node.js. You can use it to install and
publish your node programs. It manages dependencies and does other
cool stuff.

%description -l pl.UTF-8
NPM to zarządca pakietów dla node.js. Można go używać do instalowania
i publikowania kodu w Node.

%package -n bash-completion-%{name}
Summary:	bash completion for NPM commands
Summary(pl.UTF-8):	bashowe uzupełnianie parametrów dla poleceń NPM
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-%{name}
bash completion for NPM commands.

%description -n bash-completion-%{name} -l pl.UTF-8
bashowe uzupełnianie parametrów dla poleceń NPM.

%prep
%setup -qc
%{__mv} package/* .
%patch0 -p1
%patch1 -p1

grep -rl '#!.*env \(node\|python\|sh\|bash\)' . | xargs %{__sed} -i -e '1{
	s,^#!.*bin/env bash,#!%{__bash},
	s,^#!.*bin/env node,#!/usr/bin/node,
	s,^#!.*bin/env python3\?,#!%{__python3},
	s,^#!.*bin/env sh,#!%{__sh},
}'

# startup helpers we don't need
%{__rm} bin/npm bin/npm.cmd

# clean up node_modules/
for i in README.markdown LICENSE \
	.npmignore .travis.yml test examples example samples; do
	find node_modules -name $i -print0 | sort -rz | xargs -0r %{__rm} -rv
done
find node_modules -name \*.md -print0 -exec %{__rm} -v {} \;
%{__rm} lib/fetch-package-metadata.md

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

cp -a lib npmrc package.json $RPM_BUILD_ROOT%{nodejs_libdir}/npm
cp -p bin/*.js $RPM_BUILD_ROOT%{nodejs_libdir}/npm/bin
ln -s %{nodejs_libdir}/npm/bin/npm-cli.js $RPM_BUILD_ROOT%{_bindir}/npm
ln -s %{nodejs_libdir}/npm/bin/npx-cli.js $RPM_BUILD_ROOT%{_bindir}/npx

%if %{without bundled_gyp}
%{__rm} -r node_modules/node-gyp
%endif
cp -r node_modules $RPM_BUILD_ROOT%{nodejs_libdir}/npm/

# for npm help
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc
cp -a docs/content/* $RPM_BUILD_ROOT%{nodejs_libdir}/npm/doc

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

%{__mv} $RPM_BUILD_ROOT%{nodejs_libdir}/npm/lib/utils/completion.sh \
	$RPM_BUILD_ROOT/etc/bash_completion.d/%{name}.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE README.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%attr(755,root,root) %{_bindir}/npm
%attr(755,root,root) %{_bindir}/npx
%dir %{nodejs_libdir}/npm
%{nodejs_libdir}/npm/package.json
%{nodejs_libdir}/npm/npmrc

%dir %{nodejs_libdir}/npm/bin
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npm-cli.js
%attr(755,root,root) %{nodejs_libdir}/npm/bin/npx-cli.js
%dir %{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/lib/*.js
%{nodejs_libdir}/npm/lib/auth
%{nodejs_libdir}/npm/lib/config
%{nodejs_libdir}/npm/lib/doctor
%{nodejs_libdir}/npm/lib/install
%{nodejs_libdir}/npm/lib/search
%{nodejs_libdir}/npm/lib/utils
%{nodejs_libdir}/npm/node_modules

# man symlink
%{nodejs_libdir}/npm/man

%dir %{nodejs_libdir}/npm/doc
%{nodejs_libdir}/npm/doc/cli-commands
%{nodejs_libdir}/npm/doc/configuring-npm
%{nodejs_libdir}/npm/doc/using-npm

%{_mandir}/man1/npm.1*
%{_mandir}/man1/npm-*.1*
%{_mandir}/man1/npx.1*
%{_mandir}/man5/folders.5*
%{_mandir}/man5/install.5*
%{_mandir}/man5/npm*.5*
%{_mandir}/man5/package-json.5*
%{_mandir}/man5/package-lock-json.5*
%{_mandir}/man5/package-locks.5*
%{_mandir}/man5/shrinkwrap-json.5*
%{_mandir}/man7/config.7*
%{_mandir}/man7/developers.7*
%{_mandir}/man7/disputes.7*
%{_mandir}/man7/orgs.7*
%{_mandir}/man7/registry.7*
%{_mandir}/man7/removal.7*
%{_mandir}/man7/scope.7*
%{_mandir}/man7/scripts.7*
%{_mandir}/man7/semver.7*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/npm.sh
