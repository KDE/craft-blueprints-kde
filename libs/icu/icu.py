# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.svnTargets["master"] = "http://source.icu-project.org/repos/icu/icu/trunk"
        self.targetInstSrc["master"] = "source"

        for ver in ["65.1"]:
            major, minor = ver.split(".")
            self.targets[ver] = f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.tgz"
            self.targetDigestUrls[ver] = ([f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/SHASUM512.txt"], CraftHash.HashAlgorithm.SHA512)
            self.targetInstSrc[ver] = os.path.join("icu", "source")
            self.patchToApply[ver] = [("icu-msys.diff", 2)]

        for ver in ["62.1", "63.1"]:
            ver2 = ver.replace(".", "_")
            self.targets[ver] = f"http://download.icu-project.org/files/icu4c/{ver}/icu4c-{ver2}-src.tgz"
            if CraftVersion(ver) < "63.1":
                self.targetDigestUrls[ver] = ([f"https://ssl.icu-project.org/files/icu4c/{ver}/icu4c-src-{ver2}.md5"], CraftHash.HashAlgorithm.MD5)
            else:
                self.targetDigestUrls[ver] = ([f"https://ssl.icu-project.org/files/icu4c/{ver}/SHASUM512.txt"], CraftHash.HashAlgorithm.SHA512)
            if CraftVersion(ver) == "63.1":
                self.targets[ver] = f"https://files.kde.org/craft/sources/libs/icu/icu4c-{ver2}-src.tgz"
                self.targetDigestUrls[ver] = ([f"https://files.kde.org/craft/sources/libs/icu/SHASUM512.txt"], CraftHash.HashAlgorithm.SHA512)
            self.targetInstSrc[ver] = os.path.join("icu", "source")
            self.patchToApply[ver] = [("icu-msys.diff", 2)]
        self.patchToApply["63.1"] += [("icu-63.1-20181212.diff", 1),
                                     ("icu-63.1-20181215.diff", 2), # backport https://github.com/unicode-org/icu/pull/228
                                     ]
        self.defaultTarget = "63.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None

from Package.MSBuildPackageBase import *


class PackageCMake(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "allinone", "allinone.sln")

    def install(self):
        self.cleanImage()
        if not MSBuildPackageBase.install(self, installHeaders=False,
                                          buildDirs=[os.path.join(self.sourceDir(), "..", dir) for dir in
                                                     ["bin", "bin64", "lib", "lib64"]]):
            return False
        utils.copyDir(os.path.join(self.sourceDir(), "..", "include"), os.path.join(self.imageDir(), "include"))

        if CraftCore.compiler.isMSVC() and self.buildType() == "Debug":
            imagedir = os.path.join(self.installDir(), "lib")
            filelist = os.listdir(imagedir)
            for f in filelist:
                if f.endswith("d.lib"):
                    utils.copyFile(os.path.join(imagedir, f), os.path.join(imagedir, f.replace("d.lib", ".lib")))

        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False

    def make(self):
        datafile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icudt55l.dat")
        if os.path.exists(datafile):
            datafileDestination = os.path.join(self.sourceDir(), "data", "in", "icudt55l.dat")
            if os.path.exists(datafileDestination):
                os.remove(datafileDestination)
            utils.copyFile(datafile, datafileDestination)

        return AutoToolsPackageBase.make(self)

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        files = os.listdir(os.path.join(self.installDir(), "lib"))
        for dll in files:
            if dll.endswith(".dll"):
                utils.copyFile(os.path.join(self.installDir(), "lib", dll), os.path.join(self.installDir(), "bin", dll))
        return True


if CraftCore.compiler.isGCCLike():
    class PackageSuper(PackageMSys):
        pass
else:
    class PackageSuper(PackageCMake):
        pass


class Package(PackageSuper):
    def __init__(self, **args):
        PackageSuper.__init__(self)

    def postInstall(self):
        res = True
        path = os.path.join(self.installDir(), "bin/icu-config")
        if os.path.exists(path):
            res = self.patchInstallPrefix([path], self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
        return res
