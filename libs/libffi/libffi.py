import info

from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.3"]:
            self.targets[ver] = f"ftp://sourceware.org/pub/libffi/libffi-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libffi-{ver}"
        self.targetDigests["3.3"] =  (['72fba7922703ddfa7a028d513ac15a85c8d54c8d67f55fa5a4802885dc652056'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.3"] = [("libffi-3.3-20210126.diff", 1)]
        self.patchLevel["3.3"] = 2
        self.defaultTarget = "3.3"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.shell.useMSVCCompatEnv = True
        if CraftCore.compiler.isMSVC():
            wrapper = self.shell.toNativePath(self.sourceDir() / "msvcc.sh")
            self.subinfo.options.configure.args += [f"CC={wrapper} -m64", f"CXX={wrapper} -m64"]
            self.subinfo.options.configure.args += ["--enable-static", "--disable-shared"]
        else:
            self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]



