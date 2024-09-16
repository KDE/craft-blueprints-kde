from pathlib import Path

import info
import utils
from Package.MakeFilePackageBase import MakeFilePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/sparkle-project/Sparkle.git"
        for ver in ["2.5.1"]:
            self.targets[ver] = f"https://github.com/sparkle-project/Sparkle/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Sparkle-{ver}"

        self.targetDigests["2.5.1"] = (["efe2aa283e8c4f0a7ca3071bd7810f371e442ff44ebb350ad45e06cd71a59e27"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A software update framework for macOS"
        self.webpage = "https://sparkle-project.org"
        self.defaultTarget = "2.5.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(MakeFilePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True

    def make(self):
        self.cleanBuild()
        self.enterBuildDir()  # we need to call the make file in the src dir...
        return utils.system(
            [
                "xcodebuild",
                "-project",
                self.sourceDir() / "Sparkle.xcodeproj",
                "-scheme",
                "Sparkle",
                "-configuration",
                "Release",
                "-derivedDataPath",
                self.buildDir(),
                "build",
            ]
        )

    def install(self):
        self.cleanImage()
        dest = Path(self.imageDir()) / "lib"
        src = Path(self.buildDir()) / "Build/Products/Release"
        utils.createDir(dest)
        files = ["Sparkle.framework", "Sparkle.framework.dSym"]
        for f in files:
            if not utils.copyDir(src / f, dest / f):
                return False
        return True
