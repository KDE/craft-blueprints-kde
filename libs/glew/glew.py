# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "OpenGL Extension Wrangler Library"

        for ver in ["2.2.0"]:
            self.targets[ver] = f"https://github.com/nigels-com/glew/releases/download/glew-{ver}/glew-{ver}.tgz"
            self.targetInstSrc[ver] = f"glew-{ver}"
            self.targetConfigurePath[ver] = "build/cmake"
        self.patchToApply["2.2.0"] = [("fix-LNK2019.patch", 1)]

        self.targetDigests["2.2.0"] = (["d4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1"], CraftHash.HashAlgorithm.SHA256)

        self.releaseManagerId = 7878
        self.webpage = "https://github.com/nigels-com/glew"
        self.defaultTarget = "2.2.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
