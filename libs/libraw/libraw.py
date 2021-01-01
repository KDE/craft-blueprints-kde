import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.18.13'] = "https://www.libraw.org/data/LibRaw-0.18.13.tar.gz"
        self.archiveNames['0.18.13'] = "LibRaw-0.18.13.tar.gz"
        self.targetInstSrc['0.18.13'] = "LibRaw-0.18.13"
        self.patchToApply['0.18.13'] = [("LibRaw-0.18.13-20180720.diff", 1)]#https://github.com/LibRaw/LibRaw-cmake/
        self.targetDigests['0.18.13'] = (['cb1f9d0d1fabc8967d501d95c05d2b53d97a2b917345c66553b1abbea06757ca'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.18.13"] = 1
        
        # 0.20.2
        self.targets['0.20.2'] = "https://www.libraw.org/data/LibRaw-0.20.2.tar.gz"
        self.archiveNames['0.20.2'] = "LibRaw-0.20.2.tar.gz"
        self.targetInstSrc['0.20.2'] = "LibRaw-0.20.2"        
        self.targetDigests['0.20.2'] = (['dc1b486c2003435733043e4e05273477326e51c3ea554c6864a4eafaff1004a6'], CraftHash.HashAlgorithm.SHA256)

        self.description = "LibRaw is a library for reading RAW files obtained from digital photo cameras (CRW/CR2, NEF, RAF, DNG, and others)."

        self.defaultTarget = '0.18.13'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

