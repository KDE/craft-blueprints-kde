import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "FFmpeg Thumbnailer"
        self.description = "FFmpeg-based thumbnail creator for video files"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
