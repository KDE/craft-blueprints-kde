import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Libkexiv2 is a wrapper around Exiv2 library to manipulate pictures metadata as EXIF IPTC and XMP."

    def setDependencies(self):
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None


from Blueprints.CraftPackageObject import CraftPackageObject


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
