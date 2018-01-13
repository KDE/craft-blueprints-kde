import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["3.4.1"]:
            self.targets[ ver ] = f"http://ffmpeg.org/releases/ffmpeg-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"FFmpeg-{ver}"
        self.targetDigests["3.4.1"] = (['f3443e20154a590ab8a9eef7bc951e8731425efc75b44ff4bee31d8a7a574a2c'], CraftHash.HashAlgorithm.SHA256)

        self.description = "A complete, cross-platform solution to record, convert and stream audio and video."
        self.webpage = "http://ffmpeg.org/"
        self.defaultTarget = "3.4.1"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        if CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-util/nasm"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        if CraftCore.compiler.isMSVC():
            self.platform = ""
            self.subinfo.options.configure.args = f"--toolchain=msvc --enable-shared"
