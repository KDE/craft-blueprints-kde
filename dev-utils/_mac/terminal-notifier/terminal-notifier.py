import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.0.0"] = ["https://github.com/julienXX/terminal-notifier/releases/download/3.0.0/terminal-notifier-3.0.0.zip"]
        self.targetDigests["3.0.0"] = (["e804fd4727db2e146cd88edc9deb9f207a605744212c9ee386456b54f7a28dde"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstallPath["3.0.0"] = "dev-utils/bin"
        self.description = "Send User Notifications on macOS from the command-line."
        self.webpage = "https://github.com/julienXX/terminal-notifier"
        self.defaultTarget = "3.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        dev_utils = CraftCore.standardDirs.craftRoot() / "dev-utils/bin"
        return utils.createShim(dev_utils / "terminal-notifier", dev_utils / "terminal-notifier.app/Contents/MacOS/terminal-notifier")
