import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/sparkle-project/Sparkle.git"
        for ver in ["1.22.0", "1.24.0"]:
            self.svnTargets[ver] = f"[git]https://github.com/sparkle-project/Sparkle.git||{ver}"
        self.patchToApply["1.24.0"] = [("sparkle-20201119.patch", 1)]
        self.description = "A software update framework for macOS"
        self.webpage = "https://sparkle-project.org"
        self.defaultTarget = "1.24.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
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
