# RPM spec file for RedHat and Fedora
# $Id: hexen2.spec 3928 2011-03-03 09:00:20Z sezero $

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

%define use_ccache 1
%define ccachedir~/.ccache-OOo%{mdvsuffix}
%{?_with_ccache: %global use_ccache 1}
%{?_without_ccache: %global use_ccache 0}
%define debug_package            %{nil}
%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%define distsuffix mib

%ifnarch %{ix86}
%define _without_asm 1
%endif

%{?el2:%define _without_freedesktop 1}
%{?rh7:%define _without_freedesktop 1}

%{?el2:%define _without_gtk2 1}
%{?rh7:%define _without_gtk2 1}

# default build options
%{!?_without_gtk2:%define gtk1_buildopt GTK2=yes}
%{!?_without_gtk2:%define glib1_buildopt GLIB2=yes}
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
%{?_without_gtk2:%define glib1_buildopt GLIB1=yes}
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
%define prerelease	rc1

# package release number for final-release:
%define pkg_final	1
# package release number for pre-release:
%define pkg_prerel	69

Name:		hexen2
License:	GPLv2
Group:		Games/Arcade
Version:	1.5.0
Release:	%mkrel %{?prerelease:0.%{pkg_prerel}.%{prerelease}}%{!?prerelease:%{pkg_final}}
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
Group:		Games/Arcade
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

# Build xdelta
%{__make} -C libs/xdelta11 -f Makefile.xd %{glib1_buildopt}

# Launcher binaries
%{__make} -C launcher %{gtk1_buildopt}

# Build the hcode compilers
%{__make} -C utils/hcc_old
%{__make} -C utils/hcc
# Build the game-code
utils/hcc_old/hcc -src gamecode-%{gamecode_ver}/hc/h2
utils/hcc_old/hcc -src gamecode-%{gamecode_ver}/hc/h2 -name progs2.src
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/portals -oi -on
utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/hw -oi -on
#utils/bin/hcc -src gamecode-%{gamecode_ver}/hc/siege -oi -on

# Done building

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/docs
%{__install} -D -m755 engine/hexen2/h2ded %{buildroot}/%{_prefix}/games/%{name}/h2ded
%{__install} -D -m755 engine/hexen2/glhexen2 %{buildroot}/%{_prefix}/games/%{name}/glhexen2
%{__install} -D -m755 engine/hexen2/hexen2 %{buildroot}/%{_prefix}/games/%{name}/hexen2
%{__install} -D -m755 engine/hexenworld/client/hwcl %{buildroot}/%{_prefix}/games/%{name}/hwcl
%{__install} -D -m755 engine/hexenworld/client/glhwcl %{buildroot}/%{_prefix}/games/%{name}/glhwcl
%{__install} -D -m755 engine/hexenworld/server/hwsv %{buildroot}/%{_prefix}/games/%{name}/hwsv
%{__install} -D -m755 hw_utils/hwmaster/hwmaster %{buildroot}/%{_prefix}/games/%{name}/hwmaster
%{__install} -D -m755 launcher/h2launcher %{buildroot}/%{_prefix}/games/%{name}/h2launcher
# Make a symlink of the game-launcher
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__ln_s} %{_prefix}/games/hexen2/h2launcher %{buildroot}/%{_bindir}/hexen2

# Install the docs
%{__install} -D -m644 docs/README %{buildroot}/%{_prefix}/games/%{name}/docs/README
%{__install} -D -m644 docs/COPYING %{buildroot}/%{_prefix}/games/%{name}/docs/COPYING
%{__install} -D -m644 docs/BUGS %{buildroot}/%{_prefix}/games/%{name}/docs/BUGS
%{__install} -D -m644 docs/TODO %{buildroot}/%{_prefix}/games/%{name}/docs/TODO
%{__install} -D -m644 docs/ABOUT %{buildroot}/%{_prefix}/games/%{name}/docs/ABOUT
%{__install} -D -m644 docs/Features %{buildroot}/%{_prefix}/games/%{name}/docs/Features
%{__install} -D -m644 docs/CHANGES %{buildroot}/%{_prefix}/games/%{name}/docs/CHANGES
%{__install} -D -m644 docs/README.music %{buildroot}/%{_prefix}/games/%{name}/docs/README.music
%{__install} -D -m644 docs/README.3dfx %{buildroot}/%{_prefix}/games/%{name}/docs/README.3dfx
%{__install} -D -m644 docs/README.launcher %{buildroot}/%{_prefix}/games/%{name}/docs/README.launcher
%{__install} -D -m644 docs/README.hwcl %{buildroot}/%{_prefix}/games/%{name}/docs/README.hwcl
%{__install} -D -m644 docs/README.hwsv %{buildroot}/%{_prefix}/games/%{name}/docs/README.hwsv
%{__install} -D -m644 docs/README.hwmaster %{buildroot}/%{_prefix}/games/%{name}/docs/README.hwmaster
%{__install} -D -m644 docs/SrcNotes.txt %{buildroot}/%{_prefix}/games/%{name}/docs/SrcNotes.txt
%{__install} -D -m644 docs/ReleaseNotes-%{version} %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-%{version}
# install release notes for the older versions
%{__install} -D -m644 docs/ReleaseNotes-1.2.3 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.2.3
%{__install} -D -m644 docs/ReleaseNotes-1.2.4a %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.2.4a
%{__install} -D -m644 docs/ReleaseNotes-1.3.0 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.3.0
%{__install} -D -m644 docs/ReleaseNotes-1.4.0 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.0
%{__install} -D -m644 docs/ReleaseNotes-1.4.1 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.1
%{__install} -D -m644 docs/ReleaseNotes-1.4.2 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.2
%{__install} -D -m644 docs/ReleaseNotes-1.4.3 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.3
%{__install} -D -m644 docs/ReleaseNotes-1.4.4 %{buildroot}/%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.4

# Install the gamedata
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/data1/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/h2/progs.dat %{buildroot}/%{_prefix}/games/%{name}/data1/progs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/h2/progs2.dat %{buildroot}/%{_prefix}/games/%{name}/data1/progs2.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/hexen.rc %{buildroot}/%{_prefix}/games/%{name}/data1/hexen.rc
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/strings.txt %{buildroot}/%{_prefix}/games/%{name}/data1/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/h2/default.cfg %{buildroot}/%{_prefix}/games/%{name}/data1/default.cfg
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/portals/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/portals/progs.dat %{buildroot}/%{_prefix}/games/%{name}/portals/progs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/hexen.rc %{buildroot}/%{_prefix}/games/%{name}/portals/hexen.rc
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/strings.txt %{buildroot}/%{_prefix}/games/%{name}/portals/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/infolist.txt %{buildroot}/%{_prefix}/games/%{name}/portals/infolist.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/maplist.txt %{buildroot}/%{_prefix}/games/%{name}/portals/maplist.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/puzzles.txt %{buildroot}/%{_prefix}/games/%{name}/portals/puzzles.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/portals/default.cfg %{buildroot}/%{_prefix}/games/%{name}/portals/default.cfg
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/hw/
%{__install} -D -m644 gamecode-%{gamecode_ver}/hc/hw/hwprogs.dat %{buildroot}/%{_prefix}/games/%{name}/hw/hwprogs.dat
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/hw/strings.txt %{buildroot}/%{_prefix}/games/%{name}/hw/strings.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/txt/hw/default.cfg %{buildroot}/%{_prefix}/games/%{name}/hw/default.cfg
%{__install} -D -m644 hw/pak4.pak %{buildroot}/%{_prefix}/games/%{name}/hw/pak4.pak

# Install ent fixes handling map quirks
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/data1/maps/
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt5.ent %{buildroot}/%{_prefix}/games/%{name}/data1/maps/egypt5.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/egypt5.txt %{buildroot}/%{_prefix}/games/%{name}/data1/maps/egypt5.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/romeric5.ent %{buildroot}/%{_prefix}/games/%{name}/data1/maps/romeric5.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/data1/maps/romeric5.txt %{buildroot}/%{_prefix}/games/%{name}/data1/maps/romeric5.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet2.ent %{buildroot}/%{_prefix}/games/%{name}/portals/maps/tibet2.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet2.txt %{buildroot}/%{_prefix}/games/%{name}/portals/maps/tibet2.txt
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet9.ent %{buildroot}/%{_prefix}/games/%{name}/portals/maps/tibet9.ent
%{__install} -D -m644 gamecode-%{gamecode_ver}/mapfixes/portals/maps/tibet9.txt %{buildroot}/%{_prefix}/games/%{name}/portals/maps/tibet9.txt

# Install the xdelta updates
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/patchdata/
%{__mkdir_p} %{buildroot}/%{_prefix}/games/%{name}/patchdata/data1
%{__install} -D -m755 gamecode-%{gamecode_ver}/pak_v111/update_xdelta.sh %{buildroot}/%{_prefix}/games/%{name}/update_xdelta.sh
%{__install} -D -m644 gamecode-%{gamecode_ver}/pak_v111/patchdata/data1/data1pak0.xd %{buildroot}/%{_prefix}/games/%{name}/patchdata/data1/data1pak0.xd
%{__install} -D -m644 gamecode-%{gamecode_ver}/pak_v111/patchdata/data1/data1pak1.xd %{buildroot}/%{_prefix}/games/%{name}/patchdata/data1/data1pak1.xd

# Install the update-patcher binaries
%{__install} -D -m755 libs/xdelta11/xdelta %{buildroot}/%{_prefix}/games/%{name}/xdelta114

# Install the menu icon
%{__mkdir_p} %{buildroot}/%{_datadir}/pixmaps
%{__install} -D -m644 engine/resource/h2_32x32x4.png %{buildroot}/%{_datadir}/pixmaps/%{name}.png

# Install menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Hexen 2
Comment=Hexen II
Exec=hexen2
Icon=hexen2
Terminal=false
Type=Application
Encoding=UTF-8
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
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
%{_prefix}/games/%{name}/h2ded
%{_prefix}/games/%{name}/hexen2
%{_prefix}/games/%{name}/glhexen2
%{_prefix}/games/%{name}/xdelta114
%{_prefix}/games/%{name}/update_xdelta.sh
%{_prefix}/games/%{name}/patchdata/data1/data1pak0.xd
%{_prefix}/games/%{name}/patchdata/data1/data1pak1.xd
%{_prefix}/games/%{name}/data1/progs.dat
%{_prefix}/games/%{name}/data1/progs2.dat
%{_prefix}/games/%{name}/data1/hexen.rc
%{_prefix}/games/%{name}/data1/strings.txt
%{_prefix}/games/%{name}/data1/default.cfg
%{_prefix}/games/%{name}/data1/maps/egypt5.ent
%{_prefix}/games/%{name}/data1/maps/egypt5.txt
%{_prefix}/games/%{name}/data1/maps/romeric5.ent
%{_prefix}/games/%{name}/data1/maps/romeric5.txt
%{_prefix}/games/%{name}/portals/progs.dat
%{_prefix}/games/%{name}/portals/hexen.rc
%{_prefix}/games/%{name}/portals/strings.txt
%{_prefix}/games/%{name}/portals/puzzles.txt
%{_prefix}/games/%{name}/portals/infolist.txt
%{_prefix}/games/%{name}/portals/maplist.txt
%{_prefix}/games/%{name}/portals/default.cfg
%{_prefix}/games/%{name}/portals/maps/tibet2.ent
%{_prefix}/games/%{name}/portals/maps/tibet2.txt
%{_prefix}/games/%{name}/portals/maps/tibet9.ent
%{_prefix}/games/%{name}/portals/maps/tibet9.txt
%{_bindir}/hexen2
%{_datadir}/pixmaps/%{name}.png
%{_prefix}/games/%{name}/h2launcher
%{_prefix}/games/%{name}/docs/README
%{_prefix}/games/%{name}/docs/COPYING
%{_prefix}/games/%{name}/docs/BUGS
%{_prefix}/games/%{name}/docs/ABOUT
%{_prefix}/games/%{name}/docs/Features
%{_prefix}/games/%{name}/docs/CHANGES
%{_prefix}/games/%{name}/docs/README.music
%{_prefix}/games/%{name}/docs/README.launcher
%{_prefix}/games/%{name}/docs/README.3dfx
%{_prefix}/games/%{name}/docs/TODO
%{_prefix}/games/%{name}/docs/SrcNotes.txt
%{_prefix}/games/%{name}/docs/ReleaseNotes-%{version}
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.2.3
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.2.4a
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.3.0
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.0
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.1
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.2
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.3
%{_prefix}/games/%{name}/docs/ReleaseNotes-1.4.4
%{!?_without_freedesktop:%{_datadir}/applications/%{desktop_vendor}-%{name}.desktop}
%{?_without_freedesktop:%{_sysconfdir}/X11/applnk/Games/%{name}.desktop}

%files -n hexenworld
%defattr(-,root,root)
%{_prefix}/games/%{name}/hwsv
%{_prefix}/games/%{name}/hwmaster
%{_prefix}/games/%{name}/hwcl
%{_prefix}/games/%{name}/glhwcl
%{_prefix}/games/%{name}/hw/hwprogs.dat
%{_prefix}/games/%{name}/hw/pak4.pak
%{_prefix}/games/%{name}/hw/strings.txt
%{_prefix}/games/%{name}/hw/default.cfg
%{_prefix}/games/%{name}/docs/README.hwcl
%{_prefix}/games/%{name}/docs/README.hwsv
%{_prefix}/games/%{name}/docs/README.hwmaster

