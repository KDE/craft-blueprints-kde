# -*- coding: utf-8 -*-

import info
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.defaultTarget = "67.1"
        major, minor = self.defaultTarget.split(".")
        self.targets[self.defaultTarget] = f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.tgz"
        self.targetInstSrc[self.defaultTarget] = os.path.join("icu", "source")
        self.targetDigests[self.defaultTarget] = (['94a80cd6f251a53bd2a997f6f1b5ac6653fe791dfab66e1eb0227740fb86d5dc'], CraftHash.HashAlgorithm.SHA256)

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
        f = open(Path(self.buildDir()) / "data/out/tmp/dirs.timestamp", "w")
        f.write("timestamp")
        f.close()
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
