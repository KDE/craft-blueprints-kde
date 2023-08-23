import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["6.2.1"]:
            self.targets[ver] = f"https://files.jrsoftware.org/is/6/innosetup-{ver}.exe"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "innosetup")

        self.targetDigests["6.2.1"] = (["50d21aab83579245f88e2632a61b943ad47557e42b0f02e6ce2afef4cdd8deb1"], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://jrsoftware.org/isinfo.php"
        self.defaultTarget = "6.2.1"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.unpack.runInstaller = True
        self.subinfo.options.configure.args = f'/DIR="{self.workDir()}" /SILENT /CURRENTUSER'

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        CraftCore.cache.clear()
        for name in ["ISCC"]:
            if not utils.createShim(
                os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"), os.path.join(self.imageDir(), "dev-utils", "innosetup", f"{name}.exe")
            ):
                return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
