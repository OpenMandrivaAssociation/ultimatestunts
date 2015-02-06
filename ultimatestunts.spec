# Basic macros
%define tarball_version %(echo %version | sed -e 's/\\.//g')

Summary:	Remake of the DOS racing game "stunts"
Name:		ultimatestunts
Version:	0.7.7.1
Release:	3
License:	GPLv2+
Group:		Games/Arcade
Url:		http://www.ultimatestunts.nl/
Source0:	http://downloads.sourceforge.net/ultimatestunts/%{name}-srcdata-%{tarball_version}.tar.gz
Source1:	%{name}.png
Patch0:		ultimatestunts-0.7.6-gcc-4.7.patch
BuildRequires:	bison
BuildRequires:	freealut-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(vorbis)
# yes, it's strange, but the game looks for libvorbisfile.so, that's why
# we require this devel package
Requires:	pkgconfig(vorbis)

%description
A UNIX/Windows/Linux remake of the DOS car racing game "stunts", providing
modern features like openGL graphics, 3D sound and internet multiplaying.
Design your own tracks, choose your opponents and try the most spectacular
stunts you've ever seen.

%files
%defattr(0755,root,root,0755)
%{_gamesbindir}/ustunts
%{_gamesbindir}/ustunts3dedit
%{_gamesbindir}/ustuntsai
%{_gamesbindir}/ustuntsserver
%{_gamesbindir}/ustuntstrackedit
%defattr(0644,root,root,0755)
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-trackedit.desktop
%{_gamesdatadir}/ultimatestunts
%{_datadir}/pixmaps/*.png
%config %{_sysconfdir}/ultimatestunts.conf

#----------------------------------------------------------------------------

%prep
%setup -q -n ultimatestunts-srcdata-%{tarball_version}
%patch0 -p0
sed -i 's|@usdatadir@|%{_gamesdatadir}/ultimatestunts/|' ultimatestunts.conf.in

find . -name .svn | xargs rm -rf

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-rpath

make usdatadir=%{_gamesdatadir}/ultimatestunts/

%install
%makeinstall_std usdatadir=%{buildroot}%{_gamesdatadir}/ultimatestunts

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Ultimate Stunts
Comment=%{summary}
Exec=%{_gamesbindir}/ustunts
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-trackedit.desktop << EOF
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

