import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.74"]:
            # always point to the latest, if the checksum mismatches there was probably a new release
            self.targets[ver] = f"https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip"
            self.archiveNames[ver] = f"putty-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetDigests["0.74"] = (['853be2314afc33a589afc17eb7e3807de49c256d83280a6200ca51afd2b02f46'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.74"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
