# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.8.2", "0.8.4", "1.0.1"]:
            self.targets[ver] = f"https://git.kolab.org/libkolabxml/snapshot/libkolabxml-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libkolabxml-{ver}"
        self.patchToApply["0.8.2"] = [("libkolabxml-fixes.diff", 1)]
        self.patchToApply["0.8.4"] = [("libkolabxml-fixes.diff", 1)]
        self.patchToApply["1.0.1"] = [("libkolabxml-1.0.1-fixes.diff", 1)]

        self.description = "Kolab XML Format Schema Definitions Library"
        self.defaultTarget = "1.0.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/xsd"] = None
        self.buildDependencies["libs/xerces-c"] = None

        # the following runtimeDependencies are runtime runtimeDependencies for packages linking to the static! libkolabxml
        self.runtimeDependencies["libs/boost/boost-thread"] = None
        self.runtimeDependencies["libs/boost/boost-system"] = None
        self.runtimeDependencies["libs/libcurl"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DBUILD_TESTS=OFF"]
