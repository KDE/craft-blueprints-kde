import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "INDI Library"

        self.patchToApply["2.0.6"] = [("0001-patch-indiclient-include.patch", 1), ("0002-patch-indidriver-library.patch", 1), ("0003-patch-hid-iconv.patch", 1)]
        self.patchToApply["2.0.7"] = [("0010-patch-indiserver-strict.patch", 1), ("0006-patch-iconv-curl-dependencies.patch", 1)]
        self.patchToApply["2.0.8"] = [("0006-patch-iconv-curl-dependencies.patch", 1)]

    def registerOptions(self):
        self.options.dynamic.registerOption("buildClient", True)
        self.options.dynamic.registerOption("buildServer", CraftCore.compiler.platform.isMacOS or CraftCore.compiler.platform.isLinux)

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None

        if self.options.dynamic.buildClient:
            self.buildDependencies["libs/zlib"] = None

        if self.options.dynamic.buildServer:
            self.runtimeDependencies["libs/cfitsio"] = None
            self.runtimeDependencies["libs/libusb"] = None
            self.runtimeDependencies["libs/theora"] = None
            self.runtimeDependencies["libs/libcurl"] = None
            self.runtimeDependencies["libs/gsl"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/libfftw"] = None
            self.runtimeDependencies["libs/libev"] = None
            self.runtimeDependencies["libs/libxisf"] = None
            self.runtimeDependencies["libs/iconv"] = None
            if CraftCore.compiler.platform.isLinux:
                self.buildDependencies["libs/iconv"] = None
                self.buildDependencies["libs/libcurl"] = None


class Package(CraftPackageObject.get("libs/indilib").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            f"-DINDI_BUILD_SERVER={'ON' if self.subinfo.options.dynamic.buildServer else 'OFF'}",
            f"-DINDI_BUILD_DRIVERS={'ON' if self.subinfo.options.dynamic.buildServer else 'OFF'}",
            f"-DINDI_BUILD_CLIENT={'ON' if self.subinfo.options.dynamic.buildClient else 'OFF'}",
            f"-DINDI_BUILD_SERVER={'ON' if self.subinfo.options.dynamic.buildServer else 'OFF'}",
            f"-DINDI_BUILD_STATIC={'ON' if CraftCore.compiler.platform.isWindows and self.subinfo.options.dynamic.buildClient else 'OFF'}",
            f"-DINDI_BUILD_SHARED={'ON' if not CraftCore.compiler.platform.isWindows and self.subinfo.options.dynamic.buildClient else 'OFF'}",
            "-DINDI_BUILD_QT5_CLIENT=OFF",
            "-DBUILD_TESTING=OFF",
        ]

    def install(self):
        ret = super().install()
        if CraftCore.compiler.platform.isMacOS:
            self.fixLibraryFolder(self.imageDir() / "lib")
            self.fixLibraryFolder(self.imageDir() / "lib/indi/MathPlugins")
            self.fixLibraryFolder(self.imageDir() / "bin")
        return ret
