import sys

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "python support for kdevelop"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdevelop"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = "default"
        self.runtimeDependencies["binary/python-libs"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if ("Paths", "Python") in CraftCore.settings:
            python = os.path.join(CraftCore.settings.get("Paths", "Python"), f"python{CraftCore.compiler.executableSuffix}")
        if not os.path.exists(python):
            if CraftCore.compiler.isWindows:
                CraftCore.log.warning(f"Could not find {python} as provided by [Paths]Python, using {sys.executable} as a fallback")
            python = sys.executable
        self.subinfo.options.configure.args = f" -DPYTHON_EXECUTABLE=\"{python}\""
