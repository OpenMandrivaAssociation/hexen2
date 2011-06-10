# RPM spec file for RedHat and Fedora.
# $Id: hexen2.spec 4020 2011-06-05 12:10:16Z sezero $

# build options :
# --without alsa: build without alsa audio support
# --without midi: build without a midi driver support
#		 (defunct: there is no linux midi "driver" yet,
#		  midi playback is by timidity for now.)
# --without timidity: build without timidity music streaming support
# --without wavmusic: build without wav music streaming support
# --without mp3: build without mp3 music streaming support
# --with mpg123: build mp3 music streaming using libmpg123 instead of libmad
# --without ogg: build without ogg/vorbis music streaming support
# --without asm : do not use x86 assembly even on an intel cpu
# --without gtk2: do not use glib-2.x / gtk-2.x, and build the launcher against
#		  gtk-1.2
# --without freedesktop: do not use desktop-file-utils for the desktop shortcut

%ifnarch %{ix86}
%define _without_asm 1
%endif

%{?el2:%define _without_freedesktop 1}
%{?rh7:%define _without_freedesktop 1}

%{?el2:%define _without_gtk2 1}
%{?rh7:%define _without_gtk2 1}

# default build options
%{!?_without_gtk2:%define gtk1_buildopt GTK2=yes}
%{!?_without_asm:%define asm_buildopt USE_X86_ASM=yes}
%{!?_without_alsa:%define alsa_buildopt USE_ALSA=yes}
%{!?_without_midi:%define midi_buildopt USE_MIDI=yes}
%{!?_without_timidity:%define timidity_buildopt USE_CODEC_TIMIDITY=yes}
%{!?_without_wavmusic:%define wavmusic_buildopt USE_CODEC_WAVE=yes}
%{!?_with_mpg123:%define mp3_libraryopt MP3LIB=mad}
%{!?_without_mp3:%define mp3_buildopt USE_CODEC_MP3=yes}
%{!?_without_ogg:%define ogg_buildopt USE_CODEC_VORBIS=yes}
# build option overrides
%{?_without_gtk2:%define gtk1_buildopt GTK1=yes}
%{?_without_asm:%define asm_buildopt USE_X86_ASM=no}
%{?_without_alsa:%define alsa_buildopt USE_ALSA=no}
%{?_without_midi:%define midi_buildopt USE_MIDI=no}
%{?_without_timidity:%define timidity_buildopt USE_CODEC_TIMIDITY=no}
%{?_without_wavmusic:%define wavmusic_buildopt USE_CODEC_WAVE=no}
%{?_with_mpg123:%define mp3_libraryopt MP3LIB=mpg123}
%{?_without_mp3:%define mp3_buildopt USE_CODEC_MP3=no}
%{?_without_mp3:%define mp3_libraryopt MP3LIB=none}
%{?_without_ogg:%define ogg_buildopt USE_CODEC_VORBIS=no}
# all build options passed to makefile
%define engine_buildopt	%{asm_buildopt} %{alsa_buildopt} %{midi_buildopt} %{timidity_buildopt} %{wavmusic_buildopt} %{mp3_buildopt} %{mp3_libraryopt} %{ogg_buildopt}

%define desktop_vendor	uhexen2

%define gamecode_ver	1.20

# pre-release version: MAKE SURE to change this
# to an %undefine for the final realease!!
%define prerelease	rc3

# package release number for final-release:
%define pkg_final	%mkrel 0.1
# package release number for pre-release:
%define pkg_prerel	3

Name:		hexen2
License:	GPLv2
Group:		Amusements/Games
Version:	1.5.0
Release:	%{?prerelease:0.%{pkg_prerel}.%{prerelease}}%{!?prerelease:%{pkg_final}}
Summary:	Hexen II: Hammer of Thyrion
URL:		http://uhexen2.sourceforge.net/
Source:		http://download.sourceforge.net/uhexen2/hexen2source-%{version}%{?prerelease:-%{prerelease}}.tgz
#Source1:	http://download.sourceforge.net/uhexen2/gamedata-src-%{gamecode_ver}.tgz
Source1:	http://download.sourceforge.net/uhexen2/hexen2source-gamecode-%{version}%{?prerelease:-%{prerelease}}.tgz
Source2:	http://download.sourceforge.net/uhexen2/hexenworld-pakfiles-0.15.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SDL-devel >= 1.2.4
%{!?_without_mp3:BuildRequires:  %{!?_with_mpg123:libmad-devel}%{?_with_mpg123:libmpg123-devel >= 1.12.0}}
%{!?_without_ogg:BuildRequires:  libogg-devel libvorbis-devel}
%{!?_without_asm:BuildRequires:  nasm >= 0.98.38}
%{!?_without_freedesktop:BuildRequires: desktop-file-utils}
%{?_without_gtk2:BuildRequires:  gtk+-devel}
%{!?_without_gtk2:BuildRequires: gtk2-devel}
Obsoletes:	hexen2-missionpack
Requires:	SDL >= 1.2.4
# timidity++-patches requirement is non-fatal
#%{!?_without_timidity:Requires: timidity++-patches}
# these will be picked by rpm already
#%{!?_without_mp3:Requires: libmad}
#%{!?_without_ogg:Requires: libvorbis}

%description
Hexen II is a class based shooter game by Raven Software from 1997.
Hammer of Thyrion is a port of the GPL'ed source code released by
Raven. This package contains binaries that will run both the original
game and the Portal of Praevus mission pack, a dedicated server and a
launcher application which provides a GTK gui for launching different
versions of the game.

%package -n hexenworld
Group:		Amusements/Games
Summary:	HexenWorld Client and Server
Requires:	SDL >= 1.2.4
# timidity++-patches requirement is non-fatal
#%{!?_without_timidity:Requires: timidity++-patches}
# these will be picked by rpm already
#%{!?_without_mp3:Requires: libmad}
#%{!?_without_ogg:Requires: libvorbis}
Requires:	hexen2 >= 1.5.0

%description -n hexenworld
Hexen II is a class based shooter game by Raven Software from 1997.
Hammer of Thyrion is a port of the GPL'ed source code released by
Raven. HexenWorld is an extension of Hexen II with enhancements for
internet play. This package contains the files which are required to
run a HexenWorld server or client, and a master server application.

%prep
%setup -q -n hexen2source-%{version}%{?prerelease:-%{prerelease}} -a1 -a2

%build
# Build the main game binaries
%{__make} -C engine/hexen2 %{engine_buildopt} h2
%{__make} -s -C engine/hexen2 clean
%{__make} -C engine/hexen2 %{engine_buildopt} glh2
%{__make} -s -C engine/hexen2 clean
# Build the dedicated server
%{__make} -C engine/hexen2 -f Makefile.sv
# HexenWorld binaries
%{__make} -C engine/hexenworld/server
%{__make} -C engine/hexenworld/client %{engine_buildopt} hw
%{__make} -s -C engine/hexenworld/client clean
%{__make} -C engine/hexenworld/client %{engine_buildopt} glhw
# HexenWorld master server
%{__make} -C hw_utils/hwmaster

# Build h2patch
%{__make} -C h2patch

# Launcher binaries
%{__make} -C launcher %{gtk1_buildopt}

# Build the hcode compiler
%{__make} -C utils/hcc
# Build the game-code
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/h2
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/h2 -name progs2.src
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/portals -oi -on
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/hw -oi -on
#utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/siege -oi -on

# Done building

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/docs
%{__install} -D -m755 engine/hexen2/h2ded %{buildroot}/%{_gamesdatadir}/%{name}/h2ded
%{__install} -D -m755 engine/hexen2/glhexen2 %{buildroot}/%{_gamesdatadir}/%{name}/glhexen2
%{__install} -D -m755 engine/hexen2/hexen2 %{buildroot}/%{_gamesdatadir}/%{name}/hexen2
%{__install} -D -m755 engine/hexenworld/client/hwcl %{buildroot}/%{_gamesdatadir}/%{name}/hwcl
%{__install} -D -m755 engine/hexenworld/client/glhwcl %{buildroot}/%{_gamesdatadir}/%{name}/glhwcl
%{__install} -D -m755 engine/hexenworld/server/hwsv %{buildroot}/%{_gamesdatadir}/%{name}/hwsv
%{__install} -D -m755 hw_utils/hwmaster/hwmaster %{buildroot}/%{_gamesdatadir}/%{name}/hwmaster
%{__install} -D -m755 h2patch/h2patch %{buildroot}/%{_gamesdatadir}/%{name}/h2patch
%{__install} -D -m755 launcher/h2launcher %{buildroot}/%{_gamesdatadir}/%{name}/h2launcher
# Make a symlink of the game-launcher
%{__mkdir_p} %{buildroot}/%{_gamesbindir}
%{__ln_s} %{_gamesdatadir}/hexen2/h2launcher %{buildroot}/%{_gamesbindir}/hexen2

# Install the docs
%{__install} -D -m644 docs/README %{buildroot}/%{_gamesdatadir}/%{name}/docs/README
%{__install} -D -m644 docs/COPYING %{buildroot}/%{_gamesdatadir}/%{name}/docs/COPYING
%{__install} -D -m644 docs/BUGS %{buildroot}/%{_gamesdatadir}/%{name}/docs/BUGS
%{__install} -D -m644 docs/TODO %{buildroot}/%{_gamesdatadir}/%{name}/docs/TODO
%{__install} -D -m644 docs/ABOUT %{buildroot}/%{_gamesdatadir}/%{name}/docs/ABOUT
%{__install} -D -m644 docs/Features %{buildroot}/%{_gamesdatadir}/%{name}/docs/Features
%{__install} -D -m644 docs/CHANGES %{buildroot}/%{_gamesdatadir}/%{name}/docs/CHANGES
%{__install} -D -m644 docs/README.music %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.music
%{__install} -D -m644 docs/README.3dfx %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.3dfx
%{__install} -D -m644 docs/README.launcher %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.launcher
%{__install} -D -m644 docs/README.hwcl %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwcl
%{__install} -D -m644 docs/README.hwsv %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwsv
%{__install} -D -m644 docs/README.hwmaster %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwmaster
%{__install} -D -m644 docs/SrcNotes.txt %{buildroot}/%{_gamesdatadir}/%{name}/docs/SrcNotes.txt
%{__install} -D -m644 docs/ReleaseNotes-%{version} %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-%{version}
# install release notes for the older versions
%{__install} -D -m644 docs/ReleaseNotes-1.2.3 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.3
%{__install} -D -m644 docs/ReleaseNotes-1.2.4a %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.4a
%{__install} -D -m644 docs/ReleaseNotes-1.3.0 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.3.0
%{__install} -D -m644 docs/ReleaseNotes-1.4.0 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.0
%{__install} -D -m644 docs/ReleaseNotes-1.4.1 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.1
%{__install} -D -m644 docs/ReleaseNotes-1.4.2 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.2
%{__install} -D -m644 docs/ReleaseNotes-1.4.3 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.3
%{__install} -D -m644 docs/ReleaseNotes-1.4.4 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.4

# Install the gamedata
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/data1/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/h2/progs.dat %{buildroot}/%{_gamesdatadir}/%{name}/data1/progs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/h2/progs2.dat %{buildroot}/%{_gamesdatadir}/%{name}/data1/progs2.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/hexen.rc %{buildroot}/%{_gamesdatadir}/%{name}/data1/hexen.rc
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/strings.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/default.cfg %{buildroot}/%{_gamesdatadir}/%{name}/data1/default.cfg
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/portals/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/portals/progs.dat %{buildroot}/%{_gamesdatadir}/%{name}/portals/progs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/hexen.rc %{buildroot}/%{_gamesdatadir}/%{name}/portals/hexen.rc
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/strings.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/infolist.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/infolist.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/maplist.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/maplist.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/puzzles.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/puzzles.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/default.cfg %{buildroot}/%{_gamesdatadir}/%{name}/portals/default.cfg
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/hw/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/hw/hwprogs.dat %{buildroot}/%{_gamesdatadir}/%{name}/hw/hwprogs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/hw/strings.txt %{buildroot}/%{_gamesdatadir}/%{name}/hw/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/hw/default.cfg %{buildroot}/%{_gamesdatadir}/%{name}/hw/default.cfg
%{__install} -D -m644 hw/pak4.pak %{buildroot}/%{_gamesdatadir}/%{name}/hw/pak4.pak

# Install ent fixes handling map quirks
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/README.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/README.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/demo2.ent %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/demo2.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/demo2.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/demo2.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt4.ent %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/egypt4.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt4.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/egypt4.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt5.ent %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/egypt5.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt5.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/egypt5.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/romeric5.ent %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/romeric5.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/romeric5.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/romeric5.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/tower.ent %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/tower.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/tower.txt %{buildroot}/%{_gamesdatadir}/%{name}/data1/maps/tower.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/README.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/maps/README.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet2.ent %{buildroot}/%{_gamesdatadir}/%{name}/portals/maps/tibet2.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet2.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/maps/tibet2.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet9.ent %{buildroot}/%{_gamesdatadir}/%{name}/portals/maps/tibet9.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet9.txt %{buildroot}/%{_gamesdatadir}/%{name}/portals/maps/tibet9.txt

# Install the pak deltas
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/patchdat/
%{__mkdir_p} %{buildroot}/%{_gamesdatadir}/%{name}/patchdat/data1
%{__install} -D -m644 gamecode-%{gamecode_ver}/patch111/patchdat/data1/data1pk0.xd3 %{buildroot}/%{_gamesdatadir}/%{name}/patchdat/data1/data1pk0.xd3
%{__install} -D -m644 gamecode-%{gamecode_ver}/patch111/patchdat/data1/data1pk1.xd3 %{buildroot}/%{_gamesdatadir}/%{name}/patchdat/data1/data1pk1.xd3
%{__install} -D -m644 gamecode-%{gamecode_ver}/patch111/patchdat.txt %{buildroot}/%{_gamesdatadir}/%{name}/patchdat.txt

# Install the menu icon
%{__mkdir_p} %{buildroot}/%{_datadir}/pixmaps
%{__install} -D -m644 engine/resource/h2_32x32x4.png %{buildroot}/%{_datadir}/pixmaps/%{name}.png

# Install menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Hexen 2
Comment=Hexen II
Exec=hexen2
Icon=hexen2.png
Terminal=false
Type=Application
Encoding=UTF-8
Categories=Application;Game;
EOF

%if %{!?_without_freedesktop:1}0
%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install \
	--vendor %{desktop_vendor} \
	--dir %{buildroot}%{_datadir}/applications \
	%{name}.desktop
%else
%{__install} -D -m 0644 %{name}.desktop \
	%{buildroot}%{_sysconfdir}/X11/applnk/Games/%{name}.desktop
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_gamesdatadir}/%{name}/h2ded
%{_gamesdatadir}/%{name}/hexen2
%{_gamesdatadir}/%{name}/glhexen2
%{_gamesdatadir}/%{name}/h2patch
%{_gamesdatadir}/%{name}/patchdat/data1/data1pk0.xd3
%{_gamesdatadir}/%{name}/patchdat/data1/data1pk1.xd3
%{_gamesdatadir}/%{name}/patchdat.txt
%{_gamesdatadir}/%{name}/data1/progs.dat
%{_gamesdatadir}/%{name}/data1/progs2.dat
%{_gamesdatadir}/%{name}/data1/hexen.rc
%{_gamesdatadir}/%{name}/data1/strings.txt
%{_gamesdatadir}/%{name}/data1/default.cfg
%{_gamesdatadir}/%{name}/data1/maps/README.txt
%{_gamesdatadir}/%{name}/data1/maps/demo2.ent
%{_gamesdatadir}/%{name}/data1/maps/demo2.txt
%{_gamesdatadir}/%{name}/data1/maps/egypt4.ent
%{_gamesdatadir}/%{name}/data1/maps/egypt4.txt
%{_gamesdatadir}/%{name}/data1/maps/egypt5.ent
%{_gamesdatadir}/%{name}/data1/maps/egypt5.txt
%{_gamesdatadir}/%{name}/data1/maps/romeric5.ent
%{_gamesdatadir}/%{name}/data1/maps/romeric5.txt
%{_gamesdatadir}/%{name}/data1/maps/tower.ent
%{_gamesdatadir}/%{name}/data1/maps/tower.txt
%{_gamesdatadir}/%{name}/portals/progs.dat
%{_gamesdatadir}/%{name}/portals/hexen.rc
%{_gamesdatadir}/%{name}/portals/strings.txt
%{_gamesdatadir}/%{name}/portals/puzzles.txt
%{_gamesdatadir}/%{name}/portals/infolist.txt
%{_gamesdatadir}/%{name}/portals/maplist.txt
%{_gamesdatadir}/%{name}/portals/default.cfg
%{_gamesdatadir}/%{name}/portals/maps/README.txt
%{_gamesdatadir}/%{name}/portals/maps/tibet2.ent
%{_gamesdatadir}/%{name}/portals/maps/tibet2.txt
%{_gamesdatadir}/%{name}/portals/maps/tibet9.ent
%{_gamesdatadir}/%{name}/portals/maps/tibet9.txt
%{_gamesbindir}/hexen2
%{_datadir}/pixmaps/%{name}.png
%{_gamesdatadir}/%{name}/h2launcher
%{_gamesdatadir}/%{name}/docs/README
%{_gamesdatadir}/%{name}/docs/COPYING
%{_gamesdatadir}/%{name}/docs/BUGS
%{_gamesdatadir}/%{name}/docs/ABOUT
%{_gamesdatadir}/%{name}/docs/Features
%{_gamesdatadir}/%{name}/docs/CHANGES
%{_gamesdatadir}/%{name}/docs/README.music
%{_gamesdatadir}/%{name}/docs/README.launcher
%{_gamesdatadir}/%{name}/docs/README.3dfx
%{_gamesdatadir}/%{name}/docs/TODO
%{_gamesdatadir}/%{name}/docs/SrcNotes.txt
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-%{version}
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.3
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.4a
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.3.0
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.0
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.1
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.2
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.3
%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.4
%{!?_without_freedesktop:%{_datadir}/applications/%{desktop_vendor}-%{name}.desktop}
%{?_without_freedesktop:%{_sysconfdir}/X11/applnk/Games/%{name}.desktop}

%files -n hexenworld
%defattr(-,root,root)
%{_gamesdatadir}/%{name}/hwsv
%{_gamesdatadir}/%{name}/hwmaster
%{_gamesdatadir}/%{name}/hwcl
%{_gamesdatadir}/%{name}/glhwcl
%{_gamesdatadir}/%{name}/hw/hwprogs.dat
%{_gamesdatadir}/%{name}/hw/pak4.pak
%{_gamesdatadir}/%{name}/hw/strings.txt
%{_gamesdatadir}/%{name}/hw/default.cfg
%{_gamesdatadir}/%{name}/docs/README.hwcl
%{_gamesdatadir}/%{name}/docs/README.hwsv
%{_gamesdatadir}/%{name}/docs/README.hwmaster

%changelog
* Sun Jun 05 2011 O.Sezer <sezero@users.sourceforge.net> 1.5.0-0.3.rc3
- Bumped version to 1.5.0-rc3.

* Sun Jun 05 2011 O.Sezer <sezero@users.sourceforge.net>
- Build the main game progs using the new hcc tool.

* Wed Jun 01 2011 O.Sezer <sezero@users.sourceforge.net>
- Update spec file after the xdelta3/h2patch changes.

* Sat May 20 2011 O.Sezer <sezero@users.sourceforge.net>
- Install fixed entities for the tower map to handle the map's quirks.

* Wed May 04 2011 O.Sezer <sezero@users.sourceforge.net>
- Install demo2 and egypt4 entity fixes for handling map quirks.

* Sun Apr 24 2011 O.Sezer <sezero@users.sourceforge.net> 1.5.0-0.2.rc2
- Bumped version to 1.5.0-rc2.

* Tue Mar 08 2011 O.Sezer <sezero@users.sourceforge.net>
- Fix license tag as GPLv2.
- Add missing missing pack map entity fixes to the packaged files list.

* Thu Mar 03 2011 O.Sezer <sezero@users.sourceforge.net> 1.5.0-0.1.rc1
- Nasm version 0.98 can not be supported anymore due to its inability to
  handle -I arguments. Bumped the minimum required version to 0.98.38.

* Sun Feb 27 2011 O.Sezer <sezero@users.sourceforge.net>
- Add support for building against libmpg123 instead of libmad.

* Tue Jan 04 2011 O.Sezer <sezero@users.sourceforge.net>
- Install tibet2/tibet9 ent fixes for handling map quirks.

* Wed Dec 29 2010 O.Sezer <sezero@users.sourceforge.net>
- Install ent fixes handling map quirks.

* Sun Dec 19 2010 O.Sezer <sezero@users.sourceforge.net>
- Bumped version to 1.5.0-rc1.
- Added new build options after the music playback changes.
- Dropped SDL_mixer dependency which is not used anymore.
- Added README.music among the installed documents.
- Reworked the style we use for passing the build options to the makefiles.
- Fixed icon path.

* Fri Dec 17 2010 O.Sezer <sezero@users.sourceforge.net>
- Moved xdelta under the libs directory.

* Thu Nov 25 2010 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.11.pre11
- 1.4.4-pre11

* Mon Aug 23 2010 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.10.pre10
- 1.4.4-pre10

* Sat May 08 2010 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.9.pre9
- 1.4.4-pre9

* Sun Dec 27 2009 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.8.pre8
- 1.4.4-pre8

* Sun Aug 02 2009 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.7.pre7
- 1.4.4-pre7

* Mon Feb 02 2009 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.5.pre5
- 1.4.4-pre5

* Sun Jan 04 2009 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.4.pre4
- 1.4.4-pre4

* Tue Nov 18 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.3.pre3
- 1.4.4-pre3

* Sat Nov 08 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.2.pre2
- 1.4.4-pre2

* Mon Oct 27 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.4-0.1.pre1
- 1.4.4-pre1 (new prerelease version)

* Fri Apr 04 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.3-1
- 1.4.3-final.

* Tue Mar 25 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.3-0.2.rc2
- 1.4.3-rc2.

* Thu Feb 07 2008 O.Sezer <sezero@users.sourceforge.net> 1.4.3-0.1.rc1
- 1.4.3-rc1.

* Wed Feb 05 2008 O.Sezer <sezero@users.sourceforge.net>
- incremented the gamecode version number to 1.19a

* Wed Oct 03 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-1
- 1.4.2-final.

* Wed Sep 26 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0.6.rc3
- 1.4.2-rc3.

* Mon Aug 22 2007 O.Sezer <sezero@users.sourceforge.net>
- removed the .gtk1 suffix from launcher gtk-1.2 builds

* Sun Jul 22 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0.5.rc2
- 1.4.2-rc2.

* Fri Jun 15 2007 O.Sezer <sezero@users.sourceforge.net>
- The software renderer clients can now be compiled on non-intel.

* Sun May 20 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0.4.rc1
- 1.4.2-rc1.

* Tue Apr 10 2007 O.Sezer <sezero@users.sourceforge.net>
- xdelta now builds without autotools.

* Tue Apr 03 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0.3.pre3
- 1.4.2-pre3 prerelease.

* Tue Mar 20 2007 O.Sezer <sezero@users.sourceforge.net>
- xdelta version is 1.1.4: rename the binary properly.

* Tue Mar 20 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0
- 1.4.2-pre2 prerelease.

* Sun Mar 18 2007 O.Sezer <sezero@users.sourceforge.net>
- gamecode version changed to 1.17.

* Mon Feb 13 2007 O.Sezer <sezero@users.sourceforge.net> 1.4.2-0
- 1.4.2-pre1 prerelease.

* Mon Feb 05 2007 O.Sezer <sezero@users.sourceforge.net>
- xdelta is now included in the source tarball.

* Fri Dec 01 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.1-2
- Version 1.4.1-rev1 :
  - Updated to gamedata-1.16a
  - Updated to xdelta-1.1.3b
  - Updated the URLs

* Wed Oct 18 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.1-1
- Merged the hexen2 and mission pack packages.
- Added build option --without midi.
- Added build option --without alsa.
- Added build option --without asm.
- Disabled x86 assembly on non-intel cpus.
- Do not build or package the software renderer versions when not
  using x86 assembly until we fix them properly.
- Version 1.4.1-final.

* Wed Aug 14 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.1-0
- Added the dedicated server to the packaged binaries.
  1.4.1-pre8. Preparing for a future 1.4.1 release.

* Tue Apr 18 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-7
- More packaging tidy-ups for 1.4.0-final

* Sun Apr 16 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-6
- Back to xdelta: removed loki_patch. All of its fancy bloat can
  be done in a shell script, which is more customizable.

* Mon Apr 04 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-5
- Since 1.4.0-rc2 no mission pack specific binaries are needed.

* Mon Mar 26 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-4
- Moved hexenworld related documentation to the hexenworld package
  lib3dfxgamma is no longer needed. not packaging it.

* Thu Mar 02 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-3
- Added Features to the packaged documentation

* Wed Mar 01 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-2
- Updated after the utilities reorganization

* Sun Feb 12 2006 O.Sezer <sezero@users.sourceforge.net> 1.4.0-1
- Updated for 1.4.0

* Thu Aug 29 2005 O.Sezer <sezero@users.sourceforge.net> 1.3.0-2
- Patch: We need to remove OS checks from the update_h2 script

* Thu Aug 21 2005 O.Sezer <sezero@users.sourceforge.net> 1.3.0-1
- First sketchy spec file for RedHat and Fedora Core

