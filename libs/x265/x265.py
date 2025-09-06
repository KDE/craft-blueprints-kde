import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # does not build on Android out of the box
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.Android

    def setTargets(self):
        for ver in ["3.4", "3.5"]:
            self.targets[ver] = f"https://deb.debian.org/debian/pool/main/x/x265/x265_{ver}.orig.tar.gz"
            self.targetInstSrc[ver] = f"x265_{ver}/source"
            self.patchToApply[ver] = [
                ("disable-install-pdb.patch", 1)
            ]  # Adjusted version of https://github.com/microsoft/vcpkg/blob/master/ports/x265/disable-install-pdb.patch
        self.targetDigests["3.4"] = (["c2047f23a6b729e5c70280d23223cb61b57bfe4ad4e8f1471eeee2a61d148672"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.5"] = (["e70a3335cacacbba0b3a20ec6fecd6783932288ebc8163ad74bcc9606477cae8"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://bitbucket.org/multicoreware/x265_git.git"
        self.targetConfigurePath["master"] = "source"
        self.patchToApply["master"] = [
            ("disable-install-pdb.patch", 1)
        ]  # Adjusted version of https://github.com/microsoft/vcpkg/blob/master/ports/x265/disable-install-pdb.patch
        self.svnTargets["8f18e3a"] = "https://bitbucket.org/multicoreware/x265_git.git||8f18e3ad32684eee95e885e718655f93951128c3"
        self.targetConfigurePath["8f18e3a"] = "source"
        self.patchToApply["8f18e3a"] = [
            # Adjusted version of https://github.com/microsoft/vcpkg/blob/master/ports/x265/disable-install-pdb.patch
            ("disable-install-pdb.patch", 1),
            ("0001-Fix-.pc-for-msvc.patch", 1),
        ]
        self.patchLevel["8f18e3a"] = 1

        self.description = "H.265/HEVC video stream encoder"
        self.defaultTarget = "8f18e3a"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DEXPORT_C_API=ON", "-DENABLE_SHARED=ON", "-DENABLE_ASSEMBLY=ON", "-DENABLE_CLI=OFF"]
