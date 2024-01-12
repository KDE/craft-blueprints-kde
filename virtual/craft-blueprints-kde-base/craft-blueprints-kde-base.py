import info
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.1"] = ""
        self.defaultTarget = "0.1"

    def setDependencies(self):
        # The order is important
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.settings.getboolean("Compile", "UseCCache", False):
            self.buildDependencies["dev-utils/ccache"] = None


class Package(VirtualPackageBase):
    def __init__(self):
        super().__init__()
