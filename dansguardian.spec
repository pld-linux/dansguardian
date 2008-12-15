# TODO:
Summary:	Content filtering web proxy
Summary(pl.UTF-8):	Proxy WWW filtrujące treść
Name:		dansguardian
Version:	2.10.0.2
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dansguardian.org/downloads/2/Stable/%{name}-%{version}.tar.gz
# Source0-md5:	0a6c6d35c9e0c82fbc4a2150e8ffe977
Source1:	%{name}.init
Source2:	%{name}.httpd
Source3:	%{name}.lighttpd
Source4:	%{name}.logrotate
URL:		http://www.dansguardian.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clamav-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	zlib-devel
Requires:	webapps

Requires:	rc-scripts

Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapp		%{name}
%define		_webapps	/etc/webapps
%define		_webappdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
DansGuardian is a web filtering engine that checks the content within
the page itself in addition to the more traditional URL filtering.

DansGuardian is a content filtering proxy. It filters using multiple
methods, including URL and domain filtering, content phrase filtering,
PICS filtering, MIME filtering, file extension filtering, POST
filtering.

%description -l pl.UTF-8
DansGuardian to silnik filtrowania WWW sprawdzający treść na samych
stronach oprócz bardziej tradycyjnego filtrowania URL-i.

DansGuardian to proxy filtrujące treść przy użyciu wielu metod, w tym
filtrowania URL-i i domen, fraz zawartych w treści, filtrowania PICS,
filtrowania MIME, filtrowania po rozszerzeniach plików, filtrowania
POST.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--enable-pcre \
	--enable-lfs \
	--enable-clamav \
	--enable-clamd \
	--enable-icap \
	--enable-kavd \
  	--enable-commandline \
	--enable-fancydm \
	--enable-trickledm \
	--enable-ntlm \
	--enable-email \
%if %{with debug}
	--enable-segv-backtrace \
	--with-dgdebug \
%endif
	--with-proxyuser nobody \
	--with-proxygroup nobody


%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,logrotate.d} \
	   $RPM_BUILD_ROOT/var/log/dansguardian \
	   $RPM_BUILD_ROOT%{_webappdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dansguardian
install %{SOURCE2} $RPM_BUILD_ROOT%{_webappdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_webappdir}/httpd.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_webappdir}/lighttpd.conf
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%%triggerin -- lighttpd
%%webapp_register lighttpd %{_webapp}

%%triggerun -- lighttpd
%%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dansguardian
%service dansguardian restart "Dansguardian daemon"

%preun
if [ "$1" = "0" ]; then
	%service dansguardian stop
	/sbin/chkconfig --del dansguardian
fi

%files
%defattr(644,root,root,755)
%doc doc/AuthPlugins doc/ContentScanners doc/DownloadManagers doc/FAQ doc/FAQ.html doc/Plugins
%{_mandir}/man8/dansguardian.8*
%attr(754,root,root) /etc/rc.d/init.d/dansguardian
%attr(755,root,root) %{_sbindir}/dansguardian
%dir %{_datadir}/dansguardian
%{_datadir}/dansguardian/languages
%{_datadir}/dansguardian/scripts
%{_datadir}/dansguardian/transparent1x1.gif
%attr(755,root,root) %{_datadir}/dansguardian/dansguardian.pl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %{_sysconfdir}/dansguardian
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dansguardian/*.conf
%dir %{_sysconfdir}/dansguardian/authplugins
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dansguardian/authplugins/*.conf
%dir %{_sysconfdir}/dansguardian/contentscanners/
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dansguardian/contentscanners/*.conf
%dir %{_sysconfdir}/dansguardian/downloadmanagers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dansguardian/downloadmanagers/*.conf
%{_sysconfdir}/dansguardian/lists
%dir %{_webappdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappdir}/lighttpd.conf
%attr(750,root,root) %dir /var/log/dansguardian
