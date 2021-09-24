import info

class subinfo(info.infoclass):

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets( self ):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ['6.26.1']:
            self.targets[ ver ] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "mlt-" + ver
        self.targetDigests['6.26.1'] = (['8a484bbbf51f33e25312757531f3ad2ce20607149d20fcfcb40a3c1e60b20b4e'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['6.26.1'] = ("mlt-6.26-cmake-fix-win32.patch", 1)
        self.patchLevel['6.26.1'] = 1
        self.svnTargets["v6"] = "https://github.com/mltframework/mlt.git|v6"
        self.patchLevel['v6'] = 20210425
        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
        self.patchLevel['master'] = 20210924
        self.defaultTarget = "master"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None
        # self.runtimeDependencies["libs/exiv2"] = None

        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None
        self.runtimeDependencies["libs/frei0r-plugins"] = None
        self.runtimeDependencies["libs/libsdl2"] = None
        self.runtimeDependencies["libs/vidstab"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.runtimeDependencies["libs/ladspa-cmt"] = None
        self.runtimeDependencies["libs/opencv/opencv_contrib"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/jack2"] = None
            self.runtimeDependencies["libs/rubberband"] = None
            #self.runtimeDependencies["libs/ladspa-swh"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        CMakePackageBase.buildTests = False
        self.subinfo.options.configure.args += " -DMOD_DECKLINK=OFF -DWINDOWS_DEPLOY=OFF -DMOD_OPENCV=ON "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir()/"lib/mlt", self.installDir()/"plugins/mlt")
        return True

