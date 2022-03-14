import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2.2"]:
            self.targets[ver] = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libwebp-{ver}"
        self.targetDigests["1.2.2"] = (['7656532f837af5f4cec3ff6bafe552c044dc39bf453587bd5b77450802f4aee6'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.2.2"

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
