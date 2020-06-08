# -*- coding: utf-8 -*-

import info
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.svnTargets["master"] = "http://source.icu-project.org/repos/icu/icu/trunk"
        self.targetInstSrc["master"] = "source"

        for ver in ["66.1", "67.1"]:
            major, minor = ver.split(".")
            self.targets[ver] = f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.tgz"
            self.targetInstSrc[ver] = os.path.join("icu", "source")
        self.targetDigests["66.1"] = (['52a3f2209ab95559c1cf0a14f24338001f389615bf00e2585ef3dbc43ecf0a2e'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["67.1"] = (['94a80cd6f251a53bd2a997f6f1b5ac6653fe791dfab66e1eb0227740fb86d5dc'], CraftHash.HashAlgorithm.SHA256)

        for ver in ["65.1"]:
            major, minor = ver.split(".")
            self.targets[ver] = f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.tgz"
            self.targetDigestUrls[ver] = ([f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/SHASUM512.txt"], CraftHash.HashAlgorithm.SHA512)
            self.targetInstSrc[ver] = os.path.join("icu", "source")

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
        self.defaultTarget = "67.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --enable-samples --enable-release=yes --enable-debug=no "
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += " --with-data-packaging=dll"
            if CraftCore.compiler.isMSVC():
                self.subinfo.options.configure.args += " --enable-extras=no"

    def make(self):
        utils.createDir(Path(self.buildDir()) / "data/out/tmp/")
        return super().make()

    def install(self):
        if not super().install():
            return False
        files = os.listdir(os.path.join(self.installDir(), "lib"))
        for dll in files:
            if dll.endswith(".dll"):
                utils.moveFile(os.path.join(self.installDir(), "lib", dll), os.path.join(self.installDir(), "bin", dll))
        return True

    def postInstall(self):
        res = True
        path = os.path.join(self.installDir(), "bin/icu-config")
        if os.path.exists(path):
            res = self.patchInstallPrefix([path], self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
        return res
