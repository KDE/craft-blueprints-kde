# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/bagder/curl.git"
        for ver in ['7.78.0']:
            self.targets[ver] = 'https://curl.haxx.se/download/curl-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'curl-' + ver
        self.targetDigests['7.78.0'] = (['98530b317dc95ccb324bbe4f834f07bb642fbc393b794ddf3434f246a71ea44a'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a free and easy-to-use client-side URL transfer library"
        self.defaultTarget = '7.78.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None


class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
       	self.subinfo.options.useShadowBuild = False
        self.subinfo.options.package.disableBinaryCache = True #This was necessary since it kept using the other recipe's binary cache
        self.subinfo.options.configure.args += " --disable-dependency-tracking" \
        " --without-ssl" \
        " --prefix=" + prefix
