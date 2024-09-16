import os
import sys

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "python support for kdevelop"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["extragear/kdevelop/kdevelop"] = None
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        python = None
        if ("Paths", "Python") in CraftCore.settings:
            python = os.path.join(CraftCore.settings.get("Paths", "Python"), f"python{CraftCore.compiler.executableSuffix}")
        if not python or not os.path.exists(python):
            if CraftCore.compiler.platform.isWindows:
                CraftCore.log.warning(f"Could not find {python} as provided by [Paths]Python, using {sys.executable} as a fallback")
            python = sys.executable
        self.subinfo.options.configure.args = f' -DPYTHON_EXECUTABLE="{python}"'
