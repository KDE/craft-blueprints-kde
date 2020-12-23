import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['2.2'] = 'https://invent.kde.org/kdevelop/kdevelop-pg-qt.git|2.2'
        self.defaultTarget = '2.2'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
