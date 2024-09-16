import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/kdev-ruby"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.description = "ruby support for kdevelop"
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["extragear/kdevelop/kdevelop"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
