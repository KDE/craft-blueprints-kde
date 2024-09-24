# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/pcre2"] = None

    def setTargets(self):
        self.description = (
            "Grep searches one or more input files for lines containing a match to a specified pattern. By default, Grep outputs the matching lines."
        )
        for ver in ["3.7", "3.11"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/grep/grep-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"grep-{ver}"
        self.targetDigests["3.7"] = (["5c10da312460aec721984d5d83246d24520ec438dd48d7ab5a05dbc0d6d6823c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.11"] = (["1db2aedde89d0dea42b16d9528f894c8d15dae4e190b59aecc78f5a951276eab"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.11"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False

    def createPackage(self):
        # a dep of gettext but not of libintl
        self.ignoredPackages.append("libs/libxml2")
        self.addExecutableFilter(r"bin/(?!(grep)).*")
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        return super().createPackage()
