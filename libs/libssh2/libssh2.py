# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = 'https://github.com/libssh2/libssh2.git'
        for ver in ["1.10.0"]:
            self.targets[ver] = f"https://www.libssh2.org/download/libssh2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libssh2-{ver}"
        self.targetDigests["1.10.0"] = (['2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.10.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['libs/zlib'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'

from Package.CMakePackageBase import *

if not CraftCore.compiler.isGCCLike():
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            self.subinfo.options.configure.args += ["-DENABLE_ZLIB_COMPRESSION=ON",
                                                    "-DBUILD_SHARED_LIBS=ON",
                                                    "-DBUILD_EXAMPLES=OFF",
                                                    "-DBUILD_TESTING=OFF"]
else:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            # configure.ac:129: error: m4_undefine: undefined macro: backend
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
