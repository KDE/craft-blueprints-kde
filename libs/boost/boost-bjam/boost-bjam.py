import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.parent.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def install(self):
        src = CraftPackageObject.get('libs/boost/boost-headers').instance.sourceDir()

        # we rename b2 => bjam for compatibility ATM
        return utils.copyFile(
            os.path.join(src, f"b2{CraftCore.compiler.executableSuffix}"),
            os.path.join(self.imageDir(), "bin", f"bjam{CraftCore.compiler.executableSuffix}"), linkOnly=False)

    def make(self):
        if OsUtils.isUnix():
            cmd = "./bootstrap.sh  --with-toolset="
            if CraftCore.compiler.isClang():
                cmd += "clang"
            elif CraftCore.compiler.isGCC():
                cmd += "gcc"
        else:
            cmd = "bootstrap.bat "
            if CraftCore.compiler.isClang():
                cmd += "clang"
            elif CraftCore.compiler.isMinGW():
                cmd += "gcc"
            elif CraftCore.compiler.isMSVC():
                platform = str(CraftCore.compiler.getMsvcPlatformToolset())
                cmd += f"vc{platform[:2]}"
        src = CraftPackageObject.get('libs/boost/boost-headers').instance.sourceDir()
        if not utils.system(cmd, cwd=src):
            log = os.path.join(src, "bootstrap.log")
            if os.path.exists(log):
                with open(log, "rt") as txt:
                    CraftCore.log.info(txt.read())
            return False
        return True
