import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ['6.26.0']:
            self.targets[ ver ] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "mlt-" + ver
        self.targetDigests['6.26.0'] = (['06da1d4f82bcb18116ee9b0dd5252c080c181b91442cbe5783a2f3bdfd550f38'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['6.26.0'] = ("mlt-6.26.0-cmake-fix-win32.patch", 1)
        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
        self.svnTargets["v7"] = "https://github.com/mltframework/mlt.git|v7"
        self.patchLevel['master'] = 20210410
        self.defaultTarget = "6.26.0"

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
        if not CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/ladspa-sdk"] = None
            self.runtimeDependencies["libs/jack2"] = None
            self.runtimeDependencies["libs/ladspa-cmt"] = None
            self.runtimeDependencies["libs/rubberband"] = None
            self.runtimeDependencies["libs/opencv/opencv"] = None
            #self.runtimeDependencies["libs/ladspa-swh"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        CMakePackageBase.buildTests = False

