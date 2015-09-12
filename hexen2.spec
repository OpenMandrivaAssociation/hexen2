
%ifnarch %x86
%define asm_buildopt USE_X86_ASM=yes
%endif

%ifarch x86_64
%define asm_buildopt USE_X86_ASM=no
%endif


%{?el2:%define _without_freedesktop 1}
%{?rh7:%define _without_freedesktop 1}

%{?el2:%define _without_gtk2 1}
%{?rh7:%define _without_gtk2 1}

# default build options
%define gtk1_buildopt GTK2=yes
%define alsa_buildopt USE_ALSA=yes
%define midi_buildopt USE_MIDI=yes
%define timidity_buildopt USE_CODEC_TIMIDITY=yes
%define wavmusic_buildopt USE_CODEC_WAVE=yes
%define mp3_libraryopt MP3LIB=mad
%define mp3_buildopt USE_CODEC_MP3=yes
%define ogg_buildopt USE_CODEC_VORBIS=yes
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

%define gamecode_ver	1.26

# pre-release version: MAKE SURE to change this
# to an %undefine for the final realease!!
# define prerelease	rc4

# package release number for final-release:
%define pkg_final	1
# package release number for pre-release:
%define pkg_prerel	4

Name:		hexen2
License:	GPLv2
Group:		Games/Arcade
Version:	1.5.4
Release:	6
Summary:	Hexen II: Hammer of Thyrion
URL:		http://uhexen2.sourceforge.net/
Source:		http://download.sourceforge.net/uhexen2/hexen2source-%{version}.tgz
Source1:	http://download.sourceforge.net/uhexen2/hexen2source-gamecode-%{version}.tgz
Source2:	http://download.sourceforge.net/uhexen2/hexenworld-pakfiles-0.15.tgz
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:	pkgconfig(mad) libmpg123-devel >= 1.12.0
BuildRequires:	pkgconfig(ogg) libvorbis-devel
BuildRequires:	nasm >= 0.98.38
BuildRequires:	desktop-file-utils
BuildRequires:	gtk+-devel
BuildRequires:	pkgconfig(gtk+-2.0)
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
%setup -q -n hexen2source-%{version} -a1 -a2

%build
# Build the main game binaries
%{__make} -C engine/hexen2 %{engine_buildopt} DEBUG=yes h2
%{__make} -s -C engine/hexen2 clean
%{__make} -C engine/hexen2 %{engine_buildopt} DEBUG=yes glh2
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
utils/hcc/hcc -src gamecode-%{gamecode_ver}/hc/h2
utils/hcc/hcc -src gamecode-%{gamecode_ver}/hc/h2 -name progs2.src
utils/hcc/hcc -src gamecode-%{gamecode_ver}/hc/portals -oi -on
utils/hcc/hcc -src gamecode-%{gamecode_ver}/hc/hw -oi -on
utils/hcc/hcc -src gamecode-%{gamecode_ver}/hc/siege -oi -on

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
%{__install} -D -m644 docs/CHANGES %{buildroot}/%{_gamesdatadir}/%{name}/docs/CHANGES.old
%{__install} -D -m644 docs/README.music %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.music
%{__install} -D -m644 docs/README.3dfx %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.3dfx
%{__install} -D -m644 docs/README.launcher %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.launcher
%{__install} -D -m644 docs/README.hwcl %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwcl
%{__install} -D -m644 docs/README.hwsv %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwsv
%{__install} -D -m644 docs/README.hwmaster %{buildroot}/%{_gamesdatadir}/%{name}/docs/README.hwmaster
%{__install} -D -m644 docs/SrcNotes.txt %{buildroot}/%{_gamesdatadir}/%{name}/docs/SrcNotes.txt
%{__install} -D -m644 docs/ReleaseNotes %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes
# install release notes for the older versions
%{__install} -D -m644 docs/ReleaseNotes.old %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes.old
# %{__install} -D -m644 docs/ReleaseNotes-1.2.4a %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.4a
# %{__install} -D -m644 docs/ReleaseNotes-1.3.0 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.3.0
# %{__install} -D -m644 docs/ReleaseNotes-1.4.0 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.0
# %{__install} -D -m644 docs/ReleaseNotes-1.4.1 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.1
# %{__install} -D -m644 docs/ReleaseNotes-1.4.2 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.2
# %{__install} -D -m644 docs/ReleaseNotes-1.4.3 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.3
# %{__install} -D -m644 docs/ReleaseNotes-1.4.4 %{buildroot}/%{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.4

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
%{_gamesdatadir}/%{name}/docs/CHANGES.old
%{_gamesdatadir}/%{name}/docs/README.music
%{_gamesdatadir}/%{name}/docs/README.launcher
%{_gamesdatadir}/%{name}/docs/README.3dfx
%{_gamesdatadir}/%{name}/docs/TODO
%{_gamesdatadir}/%{name}/docs/SrcNotes.txt
%{_gamesdatadir}/%{name}/docs/ReleaseNotes
%{_gamesdatadir}/%{name}/docs/ReleaseNotes.old
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.2.4a
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.3.0
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.0
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.1
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.2
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.3
# %{_gamesdatadir}/%{name}/docs/ReleaseNotes-1.4.4
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
