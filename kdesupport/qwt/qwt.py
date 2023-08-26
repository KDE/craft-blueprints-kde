# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["6.1.3"]:
            self.targets[ver] = f"http://downloads.sourceforge.net/sourceforge/qwt/qwt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"qwt-{ver}"
            self.patchLevel[ver] = 1
            self.patchToApply[ver] = [("qwt-6.1.3-20180429.diff", 1)]
        self.targetDigests["6.1.3"] = (["f3ecd34e72a9a2b08422fb6c8e909ca76f4ce5fa77acad7a2883b701f4309733"], CraftHash.HashAlgorithm.SHA256)
        self.description = "The Qwt library contains GUI Components and utility classes which are primarily useful for programs with a technical background"
        self.defaultTarget = "6.1.3"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        return utils.globCopyDir(os.path.join(self.installDir(), "lib"), os.path.join(self.installDir(), "bin"), ["**/*.dll"])
