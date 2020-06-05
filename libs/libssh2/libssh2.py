# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = 'https://github.com/libssh2/libssh2.git'
        for ver in ["1.8.0", "1.9.0"]:
            self.targets[ver] = f"https://www.libssh2.org/download/libssh2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libssh2-{ver}"
        self.targetDigests["1.8.0"] = (['39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.9.0"] = (['d5fb8bd563305fd1074dda90bd053fb2d29fc4bce048d182f96eaa466dfadafd'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.9.0"] = [("libssh2-1.9.0-20200605.diff", 1)]
        self.patchLevel["1.8.0"] = 6
        self.defaultTarget = '1.9.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['libs/zlib'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'

from Package.CMakePackageBase import *

if not CraftCore.compiler.isGCCLike():
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            # the lib has no exports so we can't build it shared
            self.subinfo.options.configure.args += " -DENABLE_ZLIB_COMPRESSION=ON -DBUILD_SHARED_LIBS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF"
else:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.args = " --disable-static --enable-shared"
