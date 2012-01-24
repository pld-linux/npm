# TODO
# - man fixes: npm ERR! Error: ENOENT, no such file or directory '/usr/lib/node_modules/npm/man/man1/'
# - npm-debug.log is created with 777 perms, should respect umask instead
Summary:	A package manager for node.js
Name:		npm
Version:	1.0.106
Release:	0.6
License:	MIT License
Group:		Development/Libraries
URL:		http://npmjs.org/
Source0:	http://registry.npmjs.org/npm/-/%{name}-%{version}.tgz
# Source0-md5:	44f82461713f911d9a01f194bdc891bd
BuildRequires:	nodejs >= 0.4
Requires:	nodejs
Requires:	nodejs-abbrev >= 1.0.3
Requires:	nodejs-block-stream
Requires:	nodejs-devel
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
Requires:	nodejs-waf
Requires:	nodejs-which
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

cp -a bin lib cli.js package.json $RPM_BUILD_ROOT%{nodejs_libdir}/npm
ln -s %{nodejs_libdir}/npm/bin/npm-cli.js $RPM_BUILD_ROOT%{_bindir}/npm

# ghosted global config files
# TODO: package as files to have file permissions set
install -d $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/npmrc
touch $RPM_BUILD_ROOT%{_sysconfdir}/npmignore

# link node_modules to the right folder so global installation works
#lrwxrwxrwx    1 root    root               24 jaan  21 17:42 /usr/lib/node_modules -> /usr/lib64/../lib/nodejs
#drwxr-xr-x    2 root    root                0 jaan  21 17:42 /usr/lib/nodejs/npm
# TODO: this is wrong, the link should be in nodejs or nodejs itself patched to use lib/nodejs
#ln -s %{nodejs_libdir} $RPM_BUILD_ROOT%{_prefix}/lib/node_modules

# install to mandir
install -d $RPM_BUILD_ROOT%{_mandir}
cp -pr man/* $RPM_BUILD_ROOT%{_mandir}

# FIXME: "npm help" requires this
ln -s %{_mandir} $RPM_BUILD_ROOT%{nodejs_libdir}/npm/man

# TODO bash-completion separate package

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
%{nodejs_libdir}/npm/cli.js
%dir %{nodejs_libdir}/npm/lib
%{nodejs_libdir}/npm/lib/*.js
%{nodejs_libdir}/npm/lib/utils

# man symlink
%{nodejs_libdir}/npm/man

%if 0
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
%endif

%{_mandir}/man1/npm*
%{_mandir}/man3/npm*
