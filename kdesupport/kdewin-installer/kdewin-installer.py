import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5"] = "default"
        self.runtimeDependencies["libs/libbzip2"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/kdewin-installer'
        self.defaultTarget = 'master'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False

    def configure(self):
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.configure.args = " -DBUILD_FOR_AMAROK=ON"
        return CMakePackageBase.configure(self)
