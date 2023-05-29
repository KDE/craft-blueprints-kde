import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2.5.1"]:
            self.targets[ver] = f"http://www.alsa-project.org/files/pub/lib/alsa-lib-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"alsa-lib-{ver}"
        self.targetDigests['1.2.5.1'] = (['628421d950cecaf234de3f899d520c0a6923313c964ad751ffac081df331438e'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.2.5.1"
        self.description = "Advanced Linux Sound Architecture (ALSA)"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
