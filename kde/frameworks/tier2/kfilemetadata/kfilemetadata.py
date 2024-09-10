import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Native

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A file metadata and text extraction library"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None

        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None

        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/ebook-tools"] = None
        self.runtimeDependencies["kde/kdegraphics/kdegraphics-mobipocket"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/xattr"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
