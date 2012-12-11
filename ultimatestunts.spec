# Basic macros
%define tarball_version %(echo %version | sed -e 's/\\.//g')

Name:		ultimatestunts
Summary:	Remake of the DOS racing game "stunts"
Version:	0.7.7.1
Release:	1
License:	GPLv2+
Group:		Games/Arcade
URL:		http://www.ultimatestunts.nl/
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

%prep
%setup -q -n ultimatestunts-srcdata-%{tarball_version}
%patch0 -p0
sed -i 's|@usdatadir@|%{_gamesdatadir}/ultimatestunts/|' ultimatestunts.conf.in

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


%changelog
* Mon Nov 14 2011 Andrey Bondrov <abondrov@mandriva.org> 0.7.6.1-1mdv2011.0
+ Revision: 730564
- Actually update to 0.7.6.1

  + Alexandre Felipe Muller de Souza <alexandrefm@mandriva.com>
    - Updating the package for newer version

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 0.7.5.1-3mdv2010.0
+ Revision: 434500
- rebuild

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 0.7.5.1-2mdv2009.0
+ Revision: 261764
- rebuild

* Sat Aug 02 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.7.5.1-1mdv2009.0
+ Revision: 260513
- Updated to version 0.7.5 release 1.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix description-line-too-long

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Feb 03 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.7.4.1-1mdv2008.1
+ Revision: 161854
- new version
- add missing buildrequires on bison
- disable rpath
- parallel build is broken for now, so disable it
- fix categories in desktop files
- provide missing icon file

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu May 24 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.7.1-1.1mdv2008.0
+ Revision: 30749
- Added missing BuildRequires for mesaglu-devel.
- Added missing BuildRequires for GL-devel.
- Import ultimatestunts

