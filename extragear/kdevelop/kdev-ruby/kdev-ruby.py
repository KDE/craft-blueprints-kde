import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/kdev-ruby"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.description = "ruby support for kdevelop"
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["extragear/kdevelop/kdevelop"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
