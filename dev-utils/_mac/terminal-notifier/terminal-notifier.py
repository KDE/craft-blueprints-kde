import stat
from pathlib import Path

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2.0.0"] = ["https://github.com/julienXX/terminal-notifier/releases/download/2.0.0/terminal-notifier-2.0.0.zip"]
        self.targetDigests["2.0.0"] = (["316e767d979d12adb12c3538931b245108f8b1064af44087414c096cb3376d0c"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstallPath["2.0.0"] = "dev-utils/bin"
        self.description = "Send User Notifications on macOS from the command-line."
        self.webpage = "https://github.com/julienXX/terminal-notifier"
        self.defaultTarget = "2.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        super().__init__()

    def postInstall(self):
        dev_utils = Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/bin"
        return utils.createShim(dev_utils / "terminal-notifier", dev_utils / "terminal-notifier.app/Contents/MacOS/terminal-notifier")
