import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.6.0"]:
            self.targets[ver] = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libwebp-{ver}"
        self.targetDigests["1.6.0"] = (["e4ab7009bf0629fd11982d4c2aa83964cf244cffba7347ecd39019a9e38c4564"], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://chromium.googlesource.com/webm/libwebp/"
        self.defaultTarget = "1.6.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        # we have a circular dependency here and might link to random system libs
        # self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/giflib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # see setDependencies
        self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_TIFF=ON"]
