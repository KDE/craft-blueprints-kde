import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # cyrus-sasl on MinGW does not work out of the box. It needs someone who cares
        self.parent.package.categoryInfo.platforms &= (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.compiler.isMinGW else CraftCore.compiler.Platforms.All
        )

    def setTargets(self):
        self.description = "Cyrus SASL implementation"

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

        if CraftCore.compiler.isWindows:
            # We use the older version on Windows, because someone needs
            # to port the CMake patch to a newer version to make it work
            self.defaultTarget = "2.1.26"
        else:
            self.defaultTarget = "2.1.28"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class CMakePackage(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DSTATIC_LIBRARY=OFF"]


class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--disable-macos-framework"]


if CraftCore.compiler.isWindows:

    class Package(CMakePackage):
        pass

else:

    class Package(PackageAutotools):
        pass
