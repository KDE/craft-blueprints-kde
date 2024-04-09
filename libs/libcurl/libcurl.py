# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/bagder/curl.git"
        for ver in ["7.78.0", "7.84.0"]:
            self.targets[ver] = "https://curl.haxx.se/download/curl-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "curl-" + ver
        self.targetDigests["7.78.0"] = (["98530b317dc95ccb324bbe4f834f07bb642fbc393b794ddf3434f246a71ea44a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["7.84.0"] = (["702fb26e73190a3bd77071aa146f507b9817cc4dfce218d2ab87f00cd3bc059d"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a free and easy-to-use client-side URL transfer library"
        self.patchLevel["7.84.0"] = 1
        self.defaultTarget = "7.84.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/libssh2"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_CURL_TESTS=OFF", "-DBUILD_CURL_EXE=OFF"]
        self.subinfo.options.configure.testDefine = Arguments(["-DBUILD_CURL_TESTS=ON"])
        self.subinfo.options.configure.toolsDefine = Arguments(["-DBUILD_CURL_EXE=ON"])
        self.subinfo.options.configure.staticArgs += ["-DCURL_STATICLIB=ON"]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isLinux and self.buildType() == "Debug":
            if not utils.createSymlink(self.installDir() / "lib/libcurl-d.so", self.installDir() / "lib/libcurl.so"):
                return False
        return True
