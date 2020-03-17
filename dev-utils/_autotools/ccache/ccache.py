# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/jrosdahl/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["3.7.5", "3.7.8"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["3.7.5"] = (['058cc18a25d57c0fd9aa494efdee3cc567b1b60ba1c80a18c5a0128c23832c09'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.7.8"] = (['73def0544be250b473c717e42e785e436ab725f82bf4bde8149574312972f5de'], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "3.7.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--with-bundled-zlib "
        self.supportsCCACHE = False
