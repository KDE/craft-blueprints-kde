from pathlib import Path

import info
import utils
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/bin/snoretoast-{ver}-msvc2017_{CraftCore.compiler.architecture.bits}-cl.7z"
            self.targetDigestUrls[
                ver
            ] = f"https://download.kde.org/stable/snoretoast/{ver}/bin/snoretoast-{ver}-msvc2017_{CraftCore.compiler.architecture.bits}-cl.7z.sha256"

        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"

        self.defaultTarget = "0.7.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        files = utils.filterDirectoryContent(
            self.installDir(), whitelist=lambda x, root: Path(x).suffix in BuildSystemBase.PatchableFile, blacklist=lambda x, root: True
        )
        return self.patchInstallPrefix(
            files, oldPaths=["C:/Craft/BinaryCache/windows-msvc2017_64-cl", "C:/Craft/BinaryCache/windows-msvc2017_32-cl", self.subinfo.buildPrefix]
        )
