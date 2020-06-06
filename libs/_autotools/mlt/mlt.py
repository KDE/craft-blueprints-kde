import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = "Open source multimedia framework"
        self.webpage = "https://www.mltframework.org"
        for ver in ['6.16.0', '6.18.0', '6.20.0']:
            self.targets[ ver ] = f"https://github.com/mltframework/mlt/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "mlt-" + ver
        self.targetDigests['6.16.0'] = (['9c28e54cd3ae1d43f8d0d4a24f9cee4f4b161255a3cd2aa29061fce5d46158e6'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['6.18.0'] = (['9ea6775300b9f997460f5d6adde1ea41e525ecfd30a70b987e13800e4c387ddb'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['6.20.0'] = (['ab211e27c06c0688f9cbe2d74dc0623624ef75ea4f94eea915cdc313196be2dd'], CraftHash.HashAlgorithm.SHA256)
        self.svnTargets["master"] = "https://github.com/mltframework/mlt.git"
        self.patchLevel['master'] = 20200519
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
        self.runtimeDependencies["libs/rubberband"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
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
        self.subinfo.options.configure.cxxflags += " -std=c++11"
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.ldflags += " -liconv"
        self.subinfo.options.configure.args = " --enable-gpl --enable-gpl3 --enable-opencv --enable-sdl2 --disable-sdl --disable-rtaudio --disable-decklink --disable-gtk2"
        if CraftCore.compiler.isWindows:
            prefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
            includedir = prefix+'/include/qt5'
            libdir = prefix+'/lib'
            self.subinfo.options.configure.args += \
                f" --target-os=MinGW --qt-libdir='{libdir}' --qt-includedir='{includedir}' --disable-windeploy "

