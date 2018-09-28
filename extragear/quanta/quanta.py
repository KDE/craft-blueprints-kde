import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://gitorious.org/kdevelop/quanta.git'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["extragear/kdevelop/kdevplatform"] = None
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
