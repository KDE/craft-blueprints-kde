import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.18.4"]:
            self.targets[ver] = "https://www.cairographics.org/releases/cairo-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "cairo-" + ver
        self.targetDigests["1.18.4"] = (["445ed8208a6e4823de1226a74ca319d3600e83f6369f99b14265006599c32ccb"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Multi-platform 2D graphics library"
        self.defaultTarget = "1.18.4"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/pixman"] = None
        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["libs/glib"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # tests don't build with 1.18.4 and libspectre present
        # poppler's cairo backend needs cairo with fontconfig and freetype
        self.subinfo.options.configure.args += ["-Dtests=disabled", "-Dfreetype=enabled", "-Dfontconfig=enabled"]
