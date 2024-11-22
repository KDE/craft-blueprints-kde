import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KAddressBook"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/pim/libkleo"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/kontactinterface"] = None
        self.runtimeDependencies["kde/pim/libkdepim"] = None
        self.runtimeDependencies["kde/pim/pimcommon"] = None
        self.runtimeDependencies["kde/pim/grantleetheme"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["libs/gpgme/gpgmepp"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["website"] = "https://apps.kde.org/kaddressbook/"
        self.defines["icon"] = self.blueprintDir() / "kaddressbook.ico"
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-kaddressbook.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-kaddressbook.png"
        self.defines["shortcuts"] = [{"name": "KAddressBook", "target": "bin/kaddressbook.exe", "description": self.subinfo.description}]
        return super().createPackage()
