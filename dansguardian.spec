# TODO: pl summary & desc, logrotate. NFY
Summary:	Content filtering web proxy
Name:		dansguardian
Version:	2.8.0.4
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dansguardian.org/downloads/2/Stable/%{name}-%{version}.source.tar.gz
# Source0-md5:	91d65adf4087a863ad605dddd6e18046
Source1:	%{name}.init
Source2:	%{name}.httpd
Patch0:		%{name}-zlib.patch
Patch1:		%{name}-log.patch
URL:		http://www.dansguardian.org/
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DansGuardian is a web filtering engine that checks the content within
the page itself in addition to the more traditional URL filtering.

DansGuardian is a content filtering proxy. It filters using multiple
methods, including URL and domain filtering, content phrase filtering,
PICS filtering, MIME filtering, file extension filtering, POST
filtering.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure \
	--bindir="%{_bindir}/" \
	--cgidir="/home/services/httpd/cgi-bin/" \
	--installprefix="%{buildroot}" \
	--logdir="%{_localstatedir}/log/dansguardian/" \
	--logrotatedir="%{_sysconfdir}/logrotate.d/" \
	--mandir=%{_mandir}/ \
	--sysconfdir="%{_sysconfdir}/dansguardian/" \
	--sysvdir="%{_initrddir}/" \
	--runas_usr="nobody" \
	--runas_grp="nobody"

%{__make} "libdir=/usr/%{_lib}/"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/dansguardian/ \
	$RPM_BUILD_ROOT%{_datadir}/dansguardian/{languages,phraselists,pics,logrotation}
install -d -m0755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dansguardian
install -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/dansguardian.conf
install -D dansguardian.pl $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/dansguardian.pl
install dansguardian.conf $RPM_BUILD_ROOT%{_sysconfdir}/dansguardian/dansguardian.conf
install dansguardianf1.conf $RPM_BUILD_ROOT%{_sysconfdir}/dansguardian/dansguardianf1.conf
install pics $RPM_BUILD_ROOT%{_sysconfdir}/dansguardian/pics
install dansguardian.8 $RPM_BUILD_ROOT%{_mandir}/man8/dansguardian.8
install dansguardian $RPM_BUILD_ROOT%{_bindir}/dansguardian
install transparent1x1.gif $RPM_BUILD_ROOT%{_datadir}/dansguardian/pics/transparent1x1.gif
cp -r languages $RPM_BUILD_ROOT%{_datadir}/dansguardian
cp -r phraselists $RPM_BUILD_ROOT%{_datadir}/dansguardian
install {banned*list,exception*,grey*list,filter*list,weightedphraselist*,contentregexplist} \
$RPM_BUILD_ROOT%{_sysconfdir}/dansguardian

%post
/sbin/chkconfig --add dansguardian
if [ -r /var/lock/subsys/dansguardian ]; then
	/etc/rc.d/init.d/dansguardian restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dansguardian start\" to start DansGuardian."
fi

%preun
if [ "$1" = "0" ]; then
if [ -r /var/lock/subsys/dansguardian ]; then
 /etc/rc.d/init.d/dansguardian stop >&2
fi
/sbin/chkconfig --del dansguardian
fi

%clean
#%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc INSTALL README UPGRADING
%{_mandir}/man8/dansguardian.8*
%attr(754,root,root) /etc/rc.d/init.d/dansguardian
%attr(755,root,root) %{_bindir}/dansguardian
%attr(755,root,root) /home/services/httpd/cgi-bin/dansguardian.pl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/dansguardian.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dansguardian/*
%attr(640,root,root) %{_datadir}/dansguardian/*
