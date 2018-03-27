import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/openssl"] = "default"
        self.runtimeDependencies["libs/cyrus-sasl"] = "default"

    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.kde.org/qca.git"
        self.patchLevel["master"] = 1

        #for ver in []:
            #self.targets[ver] = f"https://download.kde.org/stable/qca-qt5/{ver}/src/qca-qt5-{ver}.tar.xz"
            #self.targetDigestUrls[ver] = f"https://download.kde.org/stable/qca-qt5/{ver}/src/qca-qt5-{ver}.tar.xz.sha256"
            #self.targetInstSrc[ver] = f"qca-qt5-{ver}"

        self.description = "Qt Cryptographic Architecture (QCA)"
        self.defaultTarget = "master"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DUSE_RELATIVE_PATHS=ON"
