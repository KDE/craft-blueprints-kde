import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Kontact"
        self.displayName = "Kontact"
        self.webpage = "https://apps.kde.org/kontact/"

    def registerOptions(self):
        self.options.dynamic.setDefault("buildTests", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/kontactinterface"] = None
        self.runtimeDependencies["kde/pim/libkdepim"] = None
        self.runtimeDependencies["kde/pim/grantleetheme"] = None
        self.runtimeDependencies["kde/pim/kdepim-runtime"] = None
        self.runtimeDependencies["kde/pim/kaddressbook"] = None
        self.runtimeDependencies["kde/pim/kdepim-addons"] = None
        self.runtimeDependencies["kde/pim/akonadi-import-wizard"] = None
        self.runtimeDependencies["kde/pim/mbox-importer"] = None
        self.runtimeDependencies["kde/pim/pim-data-exporter"] = None
        self.runtimeDependencies["kde/pim/korganizer"] = None
        self.runtimeDependencies["kde/pim/kmail-account-wizard"] = None
        self.runtimeDependencies["kde/pim/kmail"] = None
        self.runtimeDependencies["kde/pim/akonadiconsole"] = None
        self.runtimeDependencies["kde/pim/akonadiclient"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["executable"] = r"bin\\kontact.exe"
        self.defines["website"] = "https://apps.kde.org/kontact/"
        self.defines["file_types"] = [".mbox"]
        self.defines["alias"] = "kontact"
        self.defines["icon"] = self.blueprintDir() / "kontact.ico"
        self.defines["icon_png"] = self.sourceDir() / "icons/150-apps-kontact.png"
        self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-kontact.png"
        self.defines["shortcuts"] = [
            {"name": "Kontact", "target": "bin/kontact.exe", "description": self.subinfo.description},
            {"name": "KMail", "target": "bin/kmail.exe"},
            {"name": "KOrganizer", "target": "bin/korganizer.exe"},
            {"name": "KAddressbook", "target": "bin/kaddressbook.exe"},
            {"name": "mbox-importer", "target": "bin/mboximporter.exe"},
            {"name": "KMail Account Wizard", "target": "bin/accountwizard.exe"},
            {"name": "Akonadi Console", "target": "bin/akonadiconsole.exe"},
        ]
        return super().createPackage()
