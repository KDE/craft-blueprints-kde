import info


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ["3.6.2", "3.5.1", "3.7.2"]:
            self.targets[v] = "https://github.com/libarchive/libarchive/archive/v" + v + ".tar.gz"
            self.targetInstSrc[v] = "libarchive-" + v

        self.targetDigests["3.5.1"] = (["6d92e669e259a55a0119c135873469778f2718acbe605717f9d341487b4d0cba"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.6.2"] = (["652b84588488c2ff38db8f666cd7f781163f85bff4449dcb2e16d3c734f96697"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.7.2"] = (["63b40acff57467f7d3a64981d4bcff60b52f539fae7688aaaaee27a448b10266"], CraftHash.HashAlgorithm.SHA256)
        self.description = "C library and command-line tools for reading and writing tar, cpio, zip, ISO, and other archive formats"
        self.defaultTarget = "3.7.2"

    def setDependencies(self):
        self.buildDependencies["libs/liblzma"] = None
        self.buildDependencies["libs/libbzip2"] = None
        self.buildDependencies["libs/zlib"] = None
        self.buildDependencies["libs/zstd"] = None
        self.buildDependencies["libs/openssl"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["libs/pcre"] = None
        self.buildDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None
        #        self.runtimeDependencies["libs/expat"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        # use openssl for encryption
        self.subinfo.options.configure.args += ["-DENABLE_OPENSSL=ON", "-DENABLE_CNG=OFF", "-DENABLE_NETTLE=OFF", "-DENABLE_WERROR=OFF"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [f"-DCMAKE_C_FLAGS='-I {self.sourceDir()}/contrib/android/include'"]
