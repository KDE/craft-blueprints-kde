import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ["3.6.2", "3.5.1", "3.7.2"]:
            self.targets[v] = f"https://github.com/libarchive/libarchive/archive/v{v}.tar.gz"
            self.targetInstSrc[v] = "libarchive-" + v

        self.targetDigests["3.5.1"] = (["6d92e669e259a55a0119c135873469778f2718acbe605717f9d341487b4d0cba"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.6.2"] = (["652b84588488c2ff38db8f666cd7f781163f85bff4449dcb2e16d3c734f96697"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.7.2"] = (["63b40acff57467f7d3a64981d4bcff60b52f539fae7688aaaaee27a448b10266"], CraftHash.HashAlgorithm.SHA256)
        self.description = "C library and command-line tools for reading and writing tar, cpio, zip, ISO, and other archive formats"
        self.defaultTarget = "3.7.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/pcre"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None
        #        self.runtimeDependencies["libs/expat"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # use openssl for encryption
        self.subinfo.options.configure.args += [
            "-DENABLE_OPENSSL=ON",
            "-DENABLE_CNG=OFF",
            "-DENABLE_NETTLE=OFF",
            "-DENABLE_WERROR=OFF",
            "-DENABLE_LIBB2=OFF",
            "-DENABLE_LZ4=OFF",
        ]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [f"-DCMAKE_C_FLAGS='-I {self.sourceDir()}/contrib/android/include'"]
