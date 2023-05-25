import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A file metadata and text extraction library"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
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


from Blueprints.CraftPackageObject import CraftPackageObject

class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)
