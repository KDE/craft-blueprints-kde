import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/alkimia|master'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/mpir"] = "default"
        self.buildDependencies["libs/libgmp"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.description = "A library with common classes and functionality used by finance applications for the KDE SC."


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
