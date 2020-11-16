import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'frei0r plugins for VR video'
        for ver in ['2.3']:
            self.targets[ver] = "http://bitbucket.org/leo_sutic/bigsh0t/get/%s.tar.bz2" % ver
        self.targetDigests['2.3'] = (['38369f1c990da0bf82a2891f64a7ed05497b0c8034f35d3768a73c27efc60e2e'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['2.3'] = 'leo_sutic-bigsh0t-f3cc21e83eb1'
        self.patchToApply['2.3'] = [('cmake-install-plugins.patch', 0)]
        self.defaultTarget = '2.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
