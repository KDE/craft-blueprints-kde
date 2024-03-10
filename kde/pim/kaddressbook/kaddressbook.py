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
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None
        else:
            self.runtimeDependencies["kde/unreleased/kuserfeedback"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
