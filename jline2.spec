%{?_javapackages_macros:%_javapackages_macros}
Name:             jline2
Version:          2.10
Release:          8.0%{?dist}
Summary:          JLine is a Java library for handling console input

License:          BSD and ASL 2.0
URL:              https://github.com/jline/jline2

# git clone git://github.com/jline/jline2.git
# cd jline2/ && git archive --format=tar --prefix=jline-2.10/ jline-2.10 | xz > jline-2.10.tar.xz
Source0:          jline-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    junit4
BuildRequires:    jansi
BuildRequires:    fusesource-pom
BuildRequires:    maven-surefire-provider-junit4

Requires:         jpackage-utils
Requires:         java
Requires:         jansi

%description
JLine is a Java library for handling console input. It is similar
in functionality to BSD editline and GNU readline. People familiar
with the readline/editline capabilities for modern shells (such as
bash and tcsh) will find most of the command editing features of
JLine to be familiar. 

%package javadoc
Summary:          Javadocs for %{name}

Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jline-%{version}

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-site-plugin']"

# Do not import non-existing internal package
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Import-Package"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions" "<Import-Package>javax.swing;resolution:=optional,!org.fusesource.jansi.internal</Import-Package>"

# Let maven bundle plugin figure out the exports.
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Export-Package"

%build
mvn-rpmbuild install javadoc:aggregate

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
cp -p target/jline-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# Uh, oh...
# http://sourceforge.net/mailarchive/message.php?msg_id=27330388
# https://github.com/jline/jline2/commit/7a4d27430999706f0fd30b4548d5879275a88de2#pom.xml
%add_maven_depmap -v "" -a "jline:jline"

# add_maven_depmap moves actual jar into its %{_javadir}/%{name}-%{version}.jar
%if 0%{?fedora}
ln -s %{_javadir}/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%else
ln -sf %{_javadir}/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%endif

%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*
%doc CHANGELOG.md README.md LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-7
- Remove unneeded animal-sniffer BR.

* Tue Mar 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-6
- Fix OSGi metadata. Don't export packages which aren't in this
  package. Fixes RHBZ#920756.

* Mon Mar 11 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-5
- Provide %{_javadir}/%{name}.jar symlink. Fix RHBZ#919640.

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-4
- Install versioned JAR and POM
- Add missing BR: animal-sniffer
- Resolves: rhbz#911559

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.10-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-2
- Do not import non-existing org.fusesource.jansi.internal package

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-1
- Upstream release 2.10
- Removed patches, using pom macros now

* Fri Oct 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.5-7
- Fix OSGi Import-Package header so as to not import non existing
  org.fusesource.jansi.internal package.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-4
- jline.console.ConsoleReader.back should be protected instead of private [rhbz#751208]

* Wed Sep 21 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-3
- Updated license
- Removed unnecessary add_to_maven_depmap

* Thu Sep 08 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-2
- Cleaned spec

* Tue May 31 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-1
- Initial packaging
