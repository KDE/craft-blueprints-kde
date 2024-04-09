import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "INDI Library 3rd Party"

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux
        self.options.dynamic.registerOption("buildLibraries", True)

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/libgphoto2"] = None
        self.runtimeDependencies["libs/libftdi"] = None
        self.runtimeDependencies["libs/libdc1394"] = None
        self.runtimeDependencies["libs/libraw"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/librtlsdr"] = None
        self.runtimeDependencies["libs/limesuite"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None

        self.runtimeDependencies["libs/indilib/indi"] = None


class Package(CraftPackageObject.get("libs/indilib").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableStriping = True
        self.subinfo.options.configure.args += [
            # Avalon Universal Drivers is off because we do not have recipe yet for libzmq3 library.
            "-DWITH_AVALONUD=OFF",
            f"-DBUILD_LIBS={'ON' if self.subinfo.options.dynamic.buildLibraries else 'OFF'}",
        ]

    def install(self):
        ret = super.install()
        if CraftCore.compiler.isMacOS:
            self.fixLibraryFolder(self.imageDir() / "bin")
            if self.subinfo.options.dynamic.buildLibraries:
                self.fixLibraryFolder(self.imageDir() / "lib")
        return ret
