import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ["6.12.0"]:
            self.targets[ ver ] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "mlt-" + ver
        self.targetDigests['6.12.0'] = (['a4af6245f0d78f9b5d4bfdfd632d7f6a8a81e47c6eb7184fb1c040db747607ac'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['6.12.0'] = [("run-exe-from-bin.patch", 1)]
        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
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
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/vidstab"] = None
        # self.runtimeDependencies["libs/jack"] = None
        # self.runtimeDependencies["libs/ladspa-sdk"] = None
        # self.runtimeDependencies["libs/ladspa-cmt"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.platform = ""
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args = " --enable-gpl --enable-gpl3 --enable-sdl2 --disable-sdl --disable-rtaudio --disable-decklink "
        if CraftCore.compiler.isWindows:
            prefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
            includedir = prefix+'/include/qt5'
            libdir = prefix+'/lib'
            self.subinfo.options.configure.args += \
                f" --target-os=MinGW --qt-libdir='{libdir}' --qt-includedir='{includedir}' --disable-windeploy "

