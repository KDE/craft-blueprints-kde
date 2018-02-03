import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.kde.org/kdb"
        self.defaultTarget = "master"
        self.description = "A database connectivity and creation framework"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/python2"] = "default"
        self.buildDependencies["win32libs/sqlite"] = "default"
        self.buildDependencies["binary/mysql"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["frameworks/tier1/kcoreaddons"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
