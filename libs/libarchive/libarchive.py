import info


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ['2.7.0', '2.8.4', '3.3.1', "3.3.2"]:
            self.targets[v] = 'https://github.com/libarchive/libarchive/archive/v' + v + '.tar.gz'
            self.targetInstSrc[v] = 'libarchive-' + v
        self.targetDigests['2.8.4'] = 'b9cc3bbd20bd71f996be9ec738f19fda8653f7af'
        self.targetDigests['2.8.4'] = (['ff138120fe7fca1bd02bed6f06d6869c7497658904a2f8916947f9a3f3257377'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['2.8.4'] = ("libarchive-2.8.4-20101205.diff", 1)
        self.patchToApply['3.3.1'] = ("libarchive-no-fatal-warnings-in-debug-mode.diff", 1)
        self.description = "C library and command-line tools for reading and writing tar, cpio, zip, ISO, and other archive formats"
        self.defaultTarget = '3.3.1'

    def setDependencies(self):
        self.buildDependencies["libs/liblzma"] = "default"
        self.buildDependencies["libs/libbzip2"] = "default"
        self.buildDependencies["libs/zlib"] = "default"
        self.buildDependencies["libs/openssl"] = "default"
        self.buildDependencies["libs/libxml2"] = "default"
        self.buildDependencies["libs/pcre"] = "default"
        self.buildDependencies["libs/win_iconv"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        #        self.runtimeDependencies["libs/expat"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # use openssl for encryption
        self.subinfo.options.configure.args += "-DENABLE_OPENSSL=ON -DENABLE_CNG=OFF -DENABLE_NETTLE=OFF"
