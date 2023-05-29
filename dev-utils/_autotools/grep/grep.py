# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/gettext"] = None

    def setTargets(self):
        self.description = (
            "Grep searches one or more input files for lines containing a match to a specified pattern. By default, Grep outputs the matching lines."
        )
        for ver in ["3.7"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/grep/grep-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"grep-{ver}"
        self.targetDigests["3.7"] = (["5c10da312460aec721984d5d83246d24520ec438dd48d7ab5a05dbc0d6d6823c"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.7"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False

    def createPackage(self):
        self.addExecutableFilter(r"bin/(?!(grep)).*")
        self.blacklist_file.append(self.packageDir() / "blacklist.txt")
        return super().createPackage()
