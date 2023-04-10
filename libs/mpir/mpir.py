# copyright:
# Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import re

import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.0.0"]:
            self.targets[ver] = f"https://github.com/wbhart/mpir/archive/refs/tags/mpir-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpir-mpir-{ver}"
        self.targetDigests["3.0.0"] = (["86a5039badc3e6738219a262873a1db5513405e15ece9527b718fcd0fac09bb2"], CraftHash.HashAlgorithm.SHA256)
        # https://github.com/wbhart/mpir/pull/292
        self.patchToApply["3.0.0"] = [("292.diff", 1)]

        self.description = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = "3.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/yasm"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False  # ./configure doesn't support absolute paths
        abi = "ABI=64"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
            abi = "ABI=32"
            self.platform = ""
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static", "--enable-gmpcompat", "--enable-cxx", abi]


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.mpirBuildDir = os.path.join(self.sourceDir(), "build.vc15")
        self.subinfo.options.configure.projectFile = os.path.join(self.mpirBuildDir, "mpir.sln")
        self.msbuildTargets = ["dll_mpir_gc", "lib_mpir_cxx"]

    def adjustProjectFile(self):
        path = self.subinfo.options.configure.projectFile
        targets = self.msbuildTargets
        # open project file to add default build targets
        f = open(str(path), "r+")
        projectFileContents = f.readlines()
        IDS = [[] for _ in range(len(targets))]
        for i in range(len(projectFileContents)):
            for j in range(len(targets)):
                # fetch target ids, to add them latter for building
                m = re.search(targets[j] + "[^{]*{(?P<ID>[^{}]*)", projectFileContents[i])
                if m is not None:
                    IDS[j] = m.group("ID")

            if "ProjectConfigurationPlatforms" in projectFileContents[i]:
                for ID in IDS:
                    projectFileContents.insert(
                        i + 1, "{" + ID + "}.Release|Win32.Build.0 = Release|Win32\n"
                    )  # 3.0.0 version needs those lines, otherwise it won't compile anything
                    projectFileContents.insert(i + 1, "{" + ID + "}.Release|x64.Build.0 = Release|x64\n")
                    projectFileContents.insert(i + 1, "{" + ID + "}.Debug|Win32.Build.0 = Debug|Win32\n")
                    projectFileContents.insert(i + 1, "{" + ID + "}.Debug|x64.Build.0 = Debug|x64\n")
                break

        f.seek(0)
        f.write("".join(projectFileContents))
        f.close()

    def make(self):
        utils.putenv("YASMPATH", os.path.join(self.rootdir, "dev-utils", "bin"))
        self.adjustProjectFile()
        return MSBuildPackageBase.make(self)

    def install(self):
        if not MSBuildPackageBase.install(self, buildDirs=[os.path.join(self.mpirBuildDir, target) for target in self.msbuildTargets]):
            return False
        # a dirty workaround the fact that FindGMP.cmake will only look for gmp.lib
        utils.copyFile(os.path.join(self.installDir(), "lib", "mpir.lib"), os.path.join(self.installDir(), "lib", "gmp.lib"))
        return True


if CraftCore.compiler.isGCCLike():

    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)

else:

    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
