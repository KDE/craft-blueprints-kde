# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.targets['2.9.5'] = 'https://files.pythonhosted.org/packages/41/97/a2ecf6c5b291799dbd40b3d041d89b0ecdb1b43c8c2503e27991325851cd/libxml2-python3-2.9.5.tar.gz'
        self.targetInstSrc['2.9.5'] = "libxml2-python3-2.9.5"
        self.patchToApply['2.9.5'] = ("libxml2-python3-include-prefix.patch", 0)
        self.targetDigests['2.9.5'] = (['51a6f863b639ce89cdfed32d58d9d37066301c373247f1c370b10d7edebe5e65'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.9.5'

    def setDependencies(self):
        self.buildDependencies["libs/libxml2"] = None


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
