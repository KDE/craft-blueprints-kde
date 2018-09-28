import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kdb|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A database connectivity and creation framework"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/python2"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["binary/mysql"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
