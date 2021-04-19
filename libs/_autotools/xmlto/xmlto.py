import info

from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.0.28']:
            self.targets[ver] = f'https://releases.pagure.org/xmlto/xmlto-{ver}.tar.bz2'
            self.targetInstSrc[ver] = 'xmlto-' + ver
        self.targetDigests['0.0.28'] = (['1130df3a7957eb9f6f0d29e4aa1c75732a7dfb6d639be013859b5c7ec5421276'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.0.28'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)

