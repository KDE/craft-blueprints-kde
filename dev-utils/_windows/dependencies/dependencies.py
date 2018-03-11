import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.5"]:
            self.targets[ver] = f"https://github.com/lucasg/Dependencies/releases/download/v{ver}/Dependencies.zip"
            self.archiveNames[ver] = f"dependencies-{ver}.zip"
            self.targetInstallPath[ver] = "dev-utils/dependencies/"

        self.targetDigests["1.5"] = (['9c3076eae0ade70d58be596305133d7989ff17782a9b814419d3a6f2b5f8735d'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://github.com/lucasg/Dependencies"
        self.description = "A rewrite of the old legacy software \"depends.exe\" in C# for Windows devs to troubleshoot dll load dependencies issues."
        self.defaultTarget = "1.5"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "dependencies.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "dependencies", "Dependencies.exe"))
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "clrphtester.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "dependencies", "clrphtester.exe"))
        return True
