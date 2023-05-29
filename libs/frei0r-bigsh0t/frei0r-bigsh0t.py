import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'frei0r plugins for VR video'

        for ver in ['2.3', '2.5.1']:
            self.targets[ver] = "http://bitbucket.org/leo_sutic/bigsh0t/get/%s.tar.bz2" % ver

        # 2.3
        self.targetDigests['2.3'] = (['38369f1c990da0bf82a2891f64a7ed05497b0c8034f35d3768a73c27efc60e2e'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['2.3'] = 'leo_sutic-bigsh0t-f3cc21e83eb1'
        self.patchToApply['2.3'] = [('cmake-install-plugins.patch', 0)]

        # 2.5.1
        self.targetDigests['2.5.1'] = (['8c6ade9e1bca5d820948db443009da6bbec876cac8e0e2a0c5de269c577a5c32'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['2.5.1'] = 'leo_sutic-bigsh0t-dd6b0f7f2977'
        self.patchToApply['2.5.1'] = [('cmake-install-plugins-2.5.patch', 1)]
        self.patchLevel['2.5.1'] = 1

        self.defaultTarget = '2.5.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
