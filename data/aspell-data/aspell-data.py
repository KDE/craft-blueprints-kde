import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.60'] = """ http://files.kolab.org/local/windows-ce/aspell-0.60.6-data.zip"""

        self.defaultTarget = '0.60'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        utils.createDir(os.path.join(self.imageDir(), "bin", "data"))
        utils.copyDir(os.path.join(self.sourceDir(), "lib", "aspell-" + self.version),
                       os.path.join(self.imageDir(), "bin", "data", "aspell"))
        return True
