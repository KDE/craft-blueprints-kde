import info


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "5.24.3.2404"
        build = "404865"
        self.targets[ver] = f"https://downloads.activestate.com/ActivePerl/releases/{ver}/ActivePerl-{ver}-MSWin32-x64-{build}.exe"
        self.targetInstallPath[ver] = "dev-utils"
        self.targetDigestUrls[ver] = ([f"https://downloads.activestate.com/ActivePerl/releases/{ver}/SHA256SUM"],
                                       CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.unpack.runInstaller = True
        self.subinfo.options.configure.args = f"/extract {self.workDir()}"

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        dirs = os.listdir(self.workDir())
        if len(dirs) != 1:
            return False
        utils.mergeTree(os.path.join(self.workDir(), dirs[0]), self.workDir())
        _, name = os.path.split(self.subinfo.targets[self.subinfo.buildTarget])
        utils.deleteFile(os.path.join(self.sourceDir(), f"{name}.msi"))
        return True
