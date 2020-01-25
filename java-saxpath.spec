

%define		srcname		saxpath
%define		subver		FCS
%define		rel			1
Summary:	Simple API for XPath
Name:		java-saxpath
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	Apache-style
Group:		Libraries/Java
Source0:	http://sourceforge.net/projects/saxpath/files/saxpath/1.0%20FCS/%{srcname}-%{version}.tar.gz/download
# Source0-md5:	cc95ecc7dfb689a29bd42323490ee702
Patch0:		buildfix.patch
URL:		http://saxpath.org
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SAXPath project stands for Simple API for XPath. SAXPath is
similar to SAX in that the API abstracts away the details of parsing
and processing the data and provides a simple event based callback
interface. It's a very useful tool for writing XPath related
applications.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}-%{subver}

find -name '*.jar' | xargs rm

%undos build.xml
%patch0 -p1

%build
export JAVA_HOME="%{java_home}"

%ant

cd src/java
%jar cf ../../%{srcname}.src.jar $(find -name '*.java')
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc build/doc/*.* build/doc/style build/doc/images
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
