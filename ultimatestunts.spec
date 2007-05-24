# Basic macros
%define version 0.7.1
%define upstream_release 1
%define release %mkrel %upstream_release.1
%define tarball_version %(echo %version.%upstream_release | sed -e 's/\\.//g')

%define Summary Remake of the DOS racing game "stunts"

Summary:	%Summary
Name:   	ultimatestunts
Version:	%version
Release:	%release
License:	GPL
Group:  	Games/Arcade
URL:    	http://www.ultimatestunts.nl/
Source: 	http://downloads.sourceforge.net/ultimatestunts/ultimatestunts-srcdata-%tarball_version.tar.gz
BuildRoot:	%_tmppath/%name-buildroot

BuildRequires:	freealut-devel
BuildRequires:	GL-devel
BuildRequires:	mesaglu-devel
BuildRequires:	openal-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel

Requires(post,postun): desktop-common-data
# yes, it's strange, but the game looks for libvorbisfile.so, that's why
# we require this devel package
Requires:	libvorbis-devel

%description
A UNIX/Windows/Linux remake of the DOS car racing game "stunts", providing
modern features like openGL graphics, 3D sound and internet multiplaying. Design
your own tracks, choose your opponents and try the most spectacular stunts
you've ever seen.

%prep
%setup -q -n ultimatestunts-srcdata-%tarball_version
sed -i 's|@usdatadir@|%_gamesdatadir/ultimatestunts/|' ultimatestunts.conf.in

%build
%configure --bindir=%_gamesbindir
%make usdatadir=%_gamesdatadir/ultimatestunts/

%install
rm -rf %buildroot
make \
	DESTDIR=%buildroot \
	usdatadir=%buildroot/%_gamesdatadir/ultimatestunts \
	install

mkdir -p %buildroot/%_datadir/applications
cat > %buildroot/%_datadir/applications/mandriva-%name.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Ultimate Stunts
Comment=%Summary
Exec=%_gamesbindir/ustunts
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

cat > %buildroot/%_datadir/applications/mandriva-%name-trackedit.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Ultimate Stunts Track Editor
Comment=The Ultimate Stunts track editor
Exec=%_gamesbindir/ustuntstrackedit
Terminal=false
Type=Application
Categories=Graphics;3DGraphics;X-MandrivaLinux-Multimedia-Graphics;
EOF

# remove unwanted files
find %buildroot/%_gamesdatadir/ultimatestunts -type d -name CVS -print0 | \
	xargs -0 rm -rf

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %buildroot

%files
%defattr(0755,root,root,0755)
%_gamesbindir/ustunts
%_gamesbindir/ustunts3dedit
%_gamesbindir/ustuntsai
%_gamesbindir/ustuntsserver
%_gamesbindir/ustuntstrackedit
%defattr(0644,root,root,0755)
%_datadir/applications/mandriva-%name.desktop
%_datadir/applications/mandriva-%name-trackedit.desktop
%_gamesdatadir/ultimatestunts
%config %{_sysconfdir}/ultimatestunts.conf
