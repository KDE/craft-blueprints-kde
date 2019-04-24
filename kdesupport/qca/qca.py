import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/cyrus-sasl"] = None

    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.kde.org/qca.git"
        self.patchLevel["master"] = 4

        for ver in ['2.2.0']:
            self.targets[ver] = f"https://download.kde.org/stable/qca/{ver}/qca-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/qca/{ver}/qca-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"qca-{ver}"

        self.description = "Qt Cryptographic Architecture (QCA)"
        self.defaultTarget = "2.2.0"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # the cmake config is not relocatable
        self.subinfo.options.package.disableBinaryCache = True
