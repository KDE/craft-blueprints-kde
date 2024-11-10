import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KMail"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None

        self.runtimeDependencies["kde/pim/kmime"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/pim/akonadi-mime"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/kimap"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["kde/pim/kldap"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/pim/kcalutils"] = None
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = None
        self.runtimeDependencies["kde/pim/kmailtransport"] = None
        self.runtimeDependencies["kde/pim/kmail-account-wizard"] = None
        self.runtimeDependencies["kde/pim/messagelib"] = None
        self.runtimeDependencies["kde/pim/ktnef"] = None
        self.runtimeDependencies["kde/pim/kontactinterface"] = None
        self.runtimeDependencies["kde/pim/libksieve"] = None
        self.runtimeDependencies["kde/pim/mailcommon"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["kde/pim/kdepim-runtime"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kstatusnotifieritem"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["shortcuts"] = [{"name": "KMail", "target": "bin/kmail.exe", "description": self.subinfo.description}]
        return super().createPackage()
        
