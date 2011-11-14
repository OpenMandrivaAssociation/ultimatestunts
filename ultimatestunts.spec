# Basic macros
%define version 0.7.6.1
%define release %mkrel 1
%define tarball_version %(echo %version | sed -e 's/\\.//g')

Name:   	ultimatestunts
Summary:	Remake of the DOS racing game "stunts"
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:  	Games/Arcade
URL:    	http://www.ultimatestunts.nl/
Source0: 	http://downloads.sourceforge.net/ultimatestunts/%{name}-srcdata-%{tarball_version}.tar.gz
Source1:	%{name}.png
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

BuildRequires:	bison
BuildRequires:	freealut-devel
BuildRequires:	GL-devel
BuildRequires:	mesaglu-devel
BuildRequires:	openal-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	libvorbis-devel

Requires(post,postun): desktop-common-data
# yes, it's strange, but the game looks for libvorbisfile.so, that's why
# we require this devel package
Requires:	libvorbis-devel

%description
A UNIX/Windows/Linux remake of the DOS car racing game "stunts", providing
modern features like openGL graphics, 3D sound and internet multiplaying.
Design your own tracks, choose your opponents and try the most spectacular
stunts you've ever seen.

%prep
%setup -q -n ultimatestunts-srcdata-%{tarball_version}
sed -i 's|@usdatadir@|%{_gamesdatadir}/ultimatestunts/|' ultimatestunts.conf.in

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-rpath
	
%make -j1 usdatadir=%{_gamesdatadir}/ultimatestunts/

%install
rm -rf %{buildroot}
make \
	DESTDIR=%{buildroot} \
	usdatadir=%{buildroot}%{_gamesdatadir}/ultimatestunts \
	install

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Ultimate Stunts
Comment=%{summary}
Exec=%{_gamesbindir}/ustunts
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-trackedit.desktop << EOF
[Desktop Entry]
Name=Ultimate Stunts Track Editor
Comment=The Ultimate Stunts track editor
Exec=%{_gamesbindir}/ustuntstrackedit
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;3DGraphics;
EOF

# remove unwanted files
find %{buildroot}%{_gamesdatadir}/ultimatestunts -type d -name CVS -print0 | \
	xargs -0 rm -rf

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root,0755)
%{_gamesbindir}/ustunts
%{_gamesbindir}/ustunts3dedit
%{_gamesbindir}/ustuntsai
%{_gamesbindir}/ustuntsserver
%{_gamesbindir}/ustuntstrackedit
%defattr(0644,root,root,0755)
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-%{name}-trackedit.desktop
%{_gamesdatadir}/ultimatestunts
%{_datadir}/pixmaps/*.png
%config %{_sysconfdir}/ultimatestunts.conf
