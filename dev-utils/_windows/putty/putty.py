import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.71"]:
            self.targets[ver] = f"https://the.earth.li/~sgtatham/putty/{ver}/w64/putty.zip"
            self.archiveNames[ver] = f"putty-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

            self.targetDigests['0.71'] = (['eaeb59b265ca07d1214c9b67fb307c639a9b8739af4279f8eba6fa166c0f17db'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.71"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
