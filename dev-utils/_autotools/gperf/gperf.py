# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # We need this as a host tool. Craft at this point isn't set up to produce both
        # host and target binaries, so on Android we have host tools in the docker image.
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "GNU gperf is a perfect hash function generator. "
        for ver in ["3.1"]:
            self.targets[ver] = f"https://ftp.gnu.org/pub/gnu/gperf/gperf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gperf-{ver}"
        self.targetDigests["3.1"] = (["588546b945bba4b70b6a3a616e80b4ab466e3f33024a352fc2198112cdbb3ae2"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.1"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
