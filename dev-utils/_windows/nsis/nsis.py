import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"

    def setTargets(self):
        for ver in ["3.0", "3.02.1"]:
            self.targets[ver] = f"http://downloads.sourceforge.net/sourceforge/nsis/nsis-{ver}.zip"
            self.targetInstSrc[ver] = f"nsis-{ver}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "nsis")

        self.targetDigests['3.0'] = '58817baa6509ad239f6cdff90ac013689aff1902'
        self.targetDigests['3.02.1'] =  (['deef3e3d90ab1a9e0ef294fff85eead25edbcb429344ad42fc9bc42b5c3b1fb5'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '3.02.1'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        for name in ['makensis', 'makensisw', 'nsis']:
            if not utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"),
                                    os.path.join(self.imageDir(), "dev-utils", "nsis", f"{name}.exe")):
                return False
        return True
