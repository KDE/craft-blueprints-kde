import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['2.1'] = 'git://anongit.kde.org/kdevelop-pg-qt|2.1'
        self.defaultTarget = '2.1'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
