import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/cyrus-sasl"] = None

    def setTargets(self):
        self.description = "Qt Cryptographic Architecture (QCA)"

        self.svnTargets["master"] = "https://anongit.kde.org/qca.git"

        # latest stable version
        self.defaultTarget = "2.3.3"
        self.targets[self.defaultTarget] = f"https://download.kde.org/stable/qca/{self.defaultTarget}/qca-{self.defaultTarget}.tar.xz"
        self.targetDigestUrls[self.defaultTarget] = f"https://download.kde.org/stable/qca/{self.defaultTarget}/qca-{self.defaultTarget}.tar.xz.sha256"
        self.targetInstSrc[self.defaultTarget] = f"qca-{self.defaultTarget}"

        self.patchToApply[self.defaultTarget] = [("msvc.diff", 1)]
        self.patchLevel[self.defaultTarget] = 1

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # the cmake config is not relocatable
        self.subinfo.options.package.disableBinaryCache = True
