import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.package.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/boost/boost-headers"] = "default"


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def install(self):
        if OsUtils.isUnix():
            return utils.copyFile(
                os.path.join(CraftPackageObject.get('libs/boost/boost-headers').instance.sourceDir(),
                             "tools", "build", "bjam"),
                os.path.join(self.imageDir(), "bin", "bjam"))
        else:
            return utils.copyFile(
                os.path.join(CraftPackageObject.get('libs/boost/boost-headers').instance.sourceDir(),
                             "tools", "build", "bjam.exe"),
                os.path.join(self.imageDir(), "bin", "bjam.exe"))

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
        utils.system(cmd, cwd=os.path.join(CraftPackageObject.get('libs/boost/boost-headers').instance.sourceDir(),
                                           "tools", "build")) or CraftCore.log.critical(
            "command: %s failed" % (cmd))
        return True
