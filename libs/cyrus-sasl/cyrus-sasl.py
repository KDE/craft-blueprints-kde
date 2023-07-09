import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.26", "2.1.28"]:
            self.targets[ver] = f"https://github.com/cyrusimap/cyrus-sasl/releases/download/cyrus-sasl-{ver}/cyrus-sasl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"cyrus-sasl-{ver}"
            # http://www.linuxfromscratch.org/blfs/view/svn/postlfs/cyrus-sasl.html
            self.patchToApply["2.1.26"] = [("cyrus-sasl-2.1.26-fixes-3.patch", 1), ("cyrus-sasl-2.1.26-openssl-1.1.0-1.patch", 1)]
        if CraftCore.compiler.isWindows:
            self.patchToApply["2.1.26"] += [("cyrus-sasl-2.1.26.patch", 1)]
        self.targetDigests["2.1.26"] = (["8fbc5136512b59bb793657f36fadda6359cae3b08f01fd16b3d406f1345b7bc3"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["2.1.26"] = 2
        self.targetDigests["2.1.28"] = (["7ccfc6abd01ed67c1a0924b353e526f1b766b21f42d4562ee635a8ebfc5bb38c"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Cyrus SASL implementation"
        self.defaultTarget = "2.1.26"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class CMakePackage(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DSTATIC_LIBRARY=OFF"]


from Package.AutoToolsPackageBase import *


class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--disable-macos-framework"]


if CraftCore.compiler.isWindows:

    class Package(CMakePackage):
        pass

else:

    class Package(PackageAutotools):
        pass
