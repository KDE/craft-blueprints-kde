import info


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ['3.3.1', '3.3.2', '3.4.3']:
            self.targets[v] = 'https://github.com/libarchive/libarchive/archive/v' + v + '.tar.gz'
            self.targetInstSrc[v] = 'libarchive-' + v
            self.patchToApply[v] = ("libarchive-no-fatal-warnings-in-debug-mode.diff", 1)
            self.patchLevel[v] = 2

        self.targetDigests['3.4.3'] = (['19556c1c67aacdff547fd719729630444dbc7161c63eca661a310676a022bb01'], CraftHash.HashAlgorithm.SHA256)
        self.description = "C library and command-line tools for reading and writing tar, cpio, zip, ISO, and other archive formats"
        self.defaultTarget = '3.4.3'

    def setDependencies(self):
        self.buildDependencies["libs/liblzma"] = None
        self.buildDependencies["libs/libbzip2"] = None
        self.buildDependencies["libs/zlib"] = None
        self.buildDependencies["libs/openssl"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["libs/pcre"] = None
        self.buildDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None
        #        self.runtimeDependencies["libs/expat"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # use openssl for encryption
        self.subinfo.options.configure.args += "-DENABLE_OPENSSL=ON -DENABLE_CNG=OFF -DENABLE_NETTLE=OFF"
