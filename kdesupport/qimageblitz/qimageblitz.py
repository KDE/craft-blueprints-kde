import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

    def setTargets(self):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'

        self.description = "Graphical effects library for KDE4"
        self.defaultTarget = 'svnHEAD'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
