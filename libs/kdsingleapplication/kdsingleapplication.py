import io
import os
import re

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.0", "1.1.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSingleApplication/releases/download/v{ver}/kdsingleapplication-{ver}.tar.gz"
            self.targetInstSrc[ver] = "kdsingleapplication-{ver}"
        self.svnTargets["master"] = "https://github.com/KDAB/KDSingleApplication.git"

        self.targetDigests["1.0.0"] = (["c92355dc10f3ebd39363458458fb5bdd9662e080cf77d91f0437763c4d936520"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.1.0"

        self.description = "KDSingleApplication is a helper class for single-instance policy applications written by KDAB."
        self.webpage = "https://github.com/KDAB/KDSingleApplication"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-DKDSingleApplication_TESTS=ON"]

        self.subinfo.options.configure.args += ["-DKDSingleApplication_QT6=ON"]
