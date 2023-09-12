import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.parent.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = "https://www.boost.org/"

        self.description = "portable C++ libraries"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def install(self):
        src = CraftPackageObject.get("libs/boost/boost-headers").instance.sourceDir() / "tools/build/src/engine"

        # we rename b2 => bjam for compatibility ATM
        return utils.copyFile(
            os.path.join(src, f"b2{CraftCore.compiler.executableSuffix}"),
            os.path.join(self.imageDir(), "bin", f"bjam{CraftCore.compiler.executableSuffix}"),
            linkOnly=False,
        )

    def make(self):
        src = CraftPackageObject.get("libs/boost/boost-headers").instance.sourceDir() / "tools/build/src/engine"
        if CraftCore.compiler.isClang():
            toolset = "clang"
        elif CraftCore.compiler.isMinGW():
            toolset = "mingw"
        elif CraftCore.compiler.isGCC():
            toolset = "gcc"
        elif CraftCore.compiler.isMSVC():
            platform = str(CraftCore.compiler.getMsvcPlatformToolset())
            toolset = f"vc{platform[:2]}"
        if OsUtils.isUnix():
            cmd = [src / "build.sh", f"--with-toolset={toolset}"]
        else:
            cmd = [src / "build.bat", toolset]
        return utils.system(cmd, cwd=src)
