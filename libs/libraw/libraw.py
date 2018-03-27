import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.17.2'] = "http://www.libraw.org/data/LibRaw-0.17.2.tar.gz"
        self.archiveNames['0.17.2'] = "LibRaw-0.17.2.tar.gz"
        self.targetInstSrc['0.17.2'] = "LibRaw-0.17.2"
        self.patchToApply['0.17.2'] = [("LibRaw-0.17.2-20180327.diff", 1)]#https://github.com/LibRaw/LibRaw-cmake/
        self.targetDigests['0.17.2'] = (['92b0c42c7666eca9307e5e1f97d6fefc196cf0b7ee089e22880259a76fafd15c'], CraftHash.HashAlgorithm.SHA256)

        self.description = "LibRaw is a library for reading RAW files obtained from digital photo cameras (CRW/CR2, NEF, RAF, DNG, and others)."
        self.defaultTarget = '0.17.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/jasper"] = "default"
        self.runtimeDependencies["libs/lcms"] = "default"
        self.runtimeDependencies["libs/libjpeg-turbo"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

