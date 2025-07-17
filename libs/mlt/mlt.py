import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ["7.14.0"]:
            self.targets[ver] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "mlt-" + ver

        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
        self.patchLevel["master"] = 20221103
        self.svnTargets["3b42360"] = "https://github.com/mltframework/mlt.git||3b42360f6c729f12cb931ec996cc2eff27f8050e"
        self.defaultTarget = "3b42360"
        self.patchLevel["3b42360"] = 1
        if CraftCore.compiler.isWindows:
            self.patchToApply["3b42360"] = [("pi_patch.diff", 1)]
            self.patchToApply["3b42360"] += [("revert-mingw-mysy2.diff", 1)]

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None

        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libasound2"] = None
            self.runtimeDependencies["libs/libexif"] = None
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
        # dependencies for glaxnimate module
        self.runtimeDependencies["libs/libarchive"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # enable submodule checkout to get glaximate
        if not CraftCore.compiler.isAndroid:
            self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += [
            "-DMOD_DECKLINK=ON",
            "-DWINDOWS_DEPLOY=OFF",
            "-DRELOCATABLE=ON",
            "-DMOD_GDK=OFF",  # don't pull in gtk
            "-DMOD_SDL2=ON",
            "-DBUILD_TESTING=OFF",
        ]

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DMOD_RTAUDIO=OFF", "-DMOD_SOX=OFF"]

        if self.subinfo.options.isActive("libs/libarchive"):
            self.subinfo.options.configure.args += ["-DMOD_GLAXNIMATE_QT6=ON"]
        else:
            self.subinfo.options.configure.args += ["-DMOD_GLAXNIMATE_QT6=OFF"]

        if CraftCore.compiler.isMSVC():
            # TODO Fix decklink module with MSVC
            self.subinfo.options.configure.args += ["-DMOD_DECKLINK=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DMOD_DECKLINK=ON"]
            # TODO OpenCV has an issue with its installation and is hence not detected
            if self.subinfo.options.isActive("libs/opencv/opencv"):
                self.subinfo.options.configure.args += ["-DMOD_OPENCV=ON"]

        self.subinfo.options.configure.args += ["-DMOD_QT=OFF", "-DMOD_QT6=ON"]

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args += ["-DCMAKE_C_FLAGS=-Wno-incompatible-pointer-types"]
        self.subinfo.options.configure.cxxflags += " -D_XOPEN_SOURCE=700 "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/mlt", self.installDir() / "plugins/mlt")
        return True
