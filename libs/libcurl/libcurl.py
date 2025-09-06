# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # depends on libpsl which is not deployable on Android at this point
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android
        if CraftCore.compiler.platform.isAndroid:
            self.options.dynamic.setDefault("buildTools", False)

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/bagder/curl.git"
        for ver in ["7.78.0", "7.84.0", "8.13.0", "8.14.1"]:
            self.targets[ver] = f"https://curl.haxx.se/download/curl-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "curl-" + ver
        self.targetDigests["7.78.0"] = (["98530b317dc95ccb324bbe4f834f07bb642fbc393b794ddf3434f246a71ea44a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["7.84.0"] = (["702fb26e73190a3bd77071aa146f507b9817cc4dfce218d2ab87f00cd3bc059d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["8.13.0"] = (["e0d20499260760f9865cb6308928223f4e5128910310c025112f592a168e1473"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["8.14.1"] = (["5760ed3c1a6aac68793fc502114f35c3e088e8cd5c084c2d044abdf646ee48fb"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a free and easy-to-use client-side URL transfer library"
        self.patchLevel["7.84.0"] = 2
        self.defaultTarget = "8.14.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/libssh2"] = None
        self.runtimeDependencies["libs/libpsl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DCURL_DISABLE_LDAP=ON",
            "-DCURL_DISABLE_LDAPS=ON",
            f"-DBUILD_CURL_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            f"-DBUILD_CURL_EXE={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-DCURL_STATICLIB={self.subinfo.options.dynamic.buildStatic.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.platform.isLinux and self.buildType() == "Debug":
            if not utils.createSymlink(self.installDir() / "lib/libcurl-d.so", self.installDir() / "lib/libcurl.so"):
                return False
        return True
