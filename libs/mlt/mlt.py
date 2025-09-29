import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils.CraftBool import CraftBool


class subinfo(info.infoclass):
    def registerOptions(self):
        # Disable tests by default because they depend on Kwalify which we don't have in Craft
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ["7.14.0"]:
            self.targets[ver] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "mlt-" + ver

        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
        self.patchLevel["master"] = 20221103

        self.svnTargets["0e0b634"] = "https://github.com/mltframework/mlt.git||0e0b634b146483d7c0346285540658bb351cf149"
        self.defaultTarget = "0e0b634"

        self.patchToApply["0e0b634"] = []
        if CraftCore.compiler.isMinGW():
            self.patchToApply["0e0b634"] += [("pi_patch.diff", 1)]
            self.patchToApply["0e0b634"] += [("revert-mingw-mysy2.diff", 1)]

        if CraftCore.compiler.isMSVC():
            self.patchToApply["0e0b634"] += [("msvc-misc.patch", 1)]
            self.patchToApply["0e0b634"] += [("msvc-misc-02.diff", 1)]
            self.patchToApply["0e0b634"] += [("msvc-sdl2-import-export.patch", 1)]
            self.patchToApply["0e0b634"] += [("msvc-link-kdewin.patch", 1)]
            self.patchToApply["0e0b634"] += [("msvc-fix-void-pointers.diff", 1)]

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None

        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libasound2"] = None
            self.runtimeDependencies["libs/movit"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/dlfcn-win32"] = None
        # ladspa-swh currently breaks MLT, making render impossible. So disable for now
        # else:
        #    self.runtimeDependencies["libs/ladspa-swh"] = None
        if not CraftCore.compiler.isMacOS:
            # self.runtimeDependencies["libs/jack2"] = None
            self.runtimeDependencies["libs/sox"] = None
        self.runtimeDependencies["libs/rubberband"] = None
        self.runtimeDependencies["libs/frei0r-plugins"] = None
        self.runtimeDependencies["libs/libsdl2"] = None
        self.runtimeDependencies["libs/vidstab"] = None
        self.runtimeDependencies["libs/ladspa-cmt"] = None
        self.runtimeDependencies["libs/ladspa-rnnoise"] = None
        self.runtimeDependencies["libs/ladspa-tap"] = None
        self.runtimeDependencies["libs/spatialaudio"] = None
        self.runtimeDependencies["libs/lilv"] = None
        self.runtimeDependencies["libs/opencv/opencv_contrib"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/libvorbis"] = None
        self.runtimeDependencies["libs/glib"] = None
        # dependencies for glaxnimate module
        self.runtimeDependencies["libs/libarchive"] = None

        if CraftCore.compiler.isMSVC():
            self.runtimeDependencies["kdesupport/kdewin"] = None
            self.runtimeDependencies["libs/pthreads"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # enable submodule checkout to get glaximate
        if not CraftCore.compiler.isAndroid and not CraftCore.compiler.isMSVC():
            self.subinfo.options.fetch.checkoutSubmodules = True

        # General CMake switches
        self.subinfo.options.configure.args += [
            "-DWINDOWS_DEPLOY=OFF",
            "-DRELOCATABLE=ON",
            "-DBUILD_TESTS_WITH_QT6=ON",
        ]

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args += ["-DCMAKE_C_FLAGS=-Wno-incompatible-pointer-types"]

        # CMake switches for MLT modules

        # TODO OpenCV has an issue with its installation on MSVC and is hence not detected
        useOpenCV = CraftBool(self.subinfo.options.isActive("libs/opencv/opencv") and not CraftCore.compiler.isMSVC())
        useMovit = CraftBool(self.subinfo.options.isActive("libs/movit") and CraftCore.compiler.isLinux)
        useSox = CraftBool(self.subinfo.options.isActive("libs/sox") and not CraftCore.compiler.isAndroid and not CraftCore.compiler.isMacOS)
        # TODO: enable Glaxnimate on MSVC after the submodule in MLT has been updated
        useGlaxnimate = CraftBool(self.subinfo.options.isActive("libs/libarchive") and not CraftCore.compiler.isMSVC())
        # TODO: fix spatialaudio tries to link against m on MSVC
        useSpatialaudio = CraftBool(self.subinfo.options.isActive("libs/spatialaudio").asOnOff and not CraftCore.compiler.isMSVC())

        self.subinfo.options.configure.args += [
            f"-DMOD_AVFORMAT={self.subinfo.options.isActive('libs/ffmpeg').asOnOff}",
            # TODO Fix decklink module with MSVC
            f"-DMOD_DECKLINK={CraftCore.compiler.isMSVC().inverted.asOnOff}",
            f"-DMOD_FREI0R={self.subinfo.options.isActive('libs/frei0r-plugins').asOnOff}",
            # don't pull in gtk
            "-DMOD_GDK=OFF",
            f"-DMOD_GLAXNIMATE_QT6={useGlaxnimate.asOnOff}",
            # TODO Fix jackrack module with MSVC
            f"-DMOD_JACKRACK={CraftCore.compiler.isMSVC().inverted.asOnOff}",  # default: ON
            f"-DUSE_LV2={self.subinfo.options.isActive('libs/lilv').asOnOff}",
            f"-DMOD_MOVIT={useMovit.asOnOff}",
            f"-DMOD_OPENCV={useOpenCV.asOnOff}",
            # TODO Fix plus module with MSVC, it needs sys/cdefs.h in ebur128
            f"-DMOD_PLUS={CraftCore.compiler.isMSVC().inverted.asOnOff}",
            # TODO Fix plusgpl module with MSVC
            f"-DMOD_PLUSGPL={CraftCore.compiler.isMSVC().inverted.asOnOff}",
            "-DMOD_QT=OFF",
            "-DMOD_QT6=ON",
            f"-DMOD_RESAMPLE={self.subinfo.options.isActive('libs/libsamplerate').asOnOff}",
            f"-DMOD_RTAUDIO={CraftCore.compiler.isAndroid.inverted.asOnOff}",
            f"-DMOD_RUBBERBAND={self.subinfo.options.isActive('libs/rubberband').asOnOff}",
            # We don't support SDL 1 anymore, we have SDL 2
            "-DMOD_SDL1=OFF",
            f"-DMOD_SDL2={self.subinfo.options.isActive('libs/libsdl2').asOnOff}",
            f"-DMOD_SOX={useSox.asOnOff}",
            f"-DMOD_SPATIALAUDIO={useSpatialaudio.asOnOff}",
            f"-DMOD_VIDSTAB={self.subinfo.options.isActive('libs/vidstab').asOnOff}",
            # TODO Fix plusgpl module with MSVC
            f"-DMOD_XINE={CraftCore.compiler.isMSVC().inverted.asOnOff}",
            f"-DMOD_XML={self.subinfo.options.isActive('libs/libxml2').asOnOff}",
        ]

        self.subinfo.options.configure.cxxflags += " -D_XOPEN_SOURCE=700 "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/mlt", self.installDir() / "plugins/mlt")
        return True
