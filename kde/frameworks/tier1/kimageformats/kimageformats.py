import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KImageFormats"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["libs/libavif"] = None
        if CraftCore.compiler.platform.isWindows:
            self.runtimeDependencies["libs/libheif"] = None
        self.runtimeDependencies["libs/libjxl"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.platform.isWindows:
            self.subinfo.options.configure.args += ["-DKIMAGEFORMATS_HEIF=ON"]
