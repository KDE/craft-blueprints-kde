# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = 'https://github.com/libssh2/libssh2.git'
        for ver in ["1.8.0"]:
            self.targets['1.8.0'] = "https://www.libssh2.org/download/libssh2-1.8.0.tar.gz"
            self.targetInstSrc['1.8.0'] = "libssh2-1.8.0"
        if CraftCore.compiler.isMSVC():
            self.patchToApply['1.8.0'] = ('0001-Ensure-other-libraries-are-told-the-correct-linkage-.patch', 1)
        self.defaultTarget = '1.8.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['libs/zlib'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DENABLE_ZLIB_COMPRESSION=ON "
