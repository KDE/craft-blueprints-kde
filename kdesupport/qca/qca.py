import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/openssl"] = "default"
        self.runtimeDependencies["libs/cyrus-sasl"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/qca.git'
        self.description = "Qt Cryptographic Architecture (QCA)"
        self.defaultTarget = 'master'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
