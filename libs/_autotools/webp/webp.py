import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.2"]:
            self.targets[ver] = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libwebp-{ver}"
        self.targetDigests["1.0.2"] = (['3d47b48c40ed6476e8047b2ddb81d93835e0ca1b8d3e8c679afbb3004dd564b1'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.0.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/giflib"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += "--disable-static --enable-shared --enable-libwebpmux"
