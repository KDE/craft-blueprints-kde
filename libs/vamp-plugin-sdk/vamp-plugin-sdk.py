import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.9.0"]:
            self.targets[ver] = f"https://code.soundsoftware.ac.uk/attachments/download/2588/vamp-plugin-sdk-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"vamp-plugin-sdk-{ver}"
        self.targetDigests["2.9.0"] = (["b72a78ef8ff8a927dc2ed7e66ecf4c62d23268a5d74d02da25be2b8d00341099"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.9.0"] = [("build-dynamic-sdk-plugins-only.patch", 0)]
        # self.svnTargets['master'] = "https://code.soundsoftware.ac.uk/hg/vamp-plugin-sdk"

        self.description = "audio analysis plugins system"
        self.webpage = "https://www.vamp-plugins.org"
        self.defaultTarget = "2.9.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-programs"]


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.projectFile = self.sourceDir() / "build/VampSDK.sln"

    def install(self):
        return super.install(installHeaders=False, buildDirs=[self.sourceDir() / "build"])


if CraftCore.compiler.isGCCLike():

    class Package(PackageAutoTools):
        def __init__(self):
            PackageAutoTools.__init__(self)

else:

    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
