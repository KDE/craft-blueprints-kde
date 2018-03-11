# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.2.1'] = "http://mesh.dl.sourceforge.net/sourceforge/openslp/openslp-1.2.1.tar.gz"
        self.targetInstSrc['1.2.1'] = "openslp-1.2.1"
        self.targetDigests['1.2.1'] = '47ab19154084d2b467f09525f5351e9ab7193cf9'
        self.patchToApply['1.2.1'] = ("openslp-1.2.1-20110814.diff", 1)
        self.description = "openslp daemon and libraries"
        self.defaultTarget = '1.2.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
