import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/pim/kalendar.git"
        self.defaultTarget = "master"
        self.description = "Calendar application"
        self.webpage = "https://invent.kde.org/pim/kalendar"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kpeople"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/pim/calendarsupport"] = None
        self.runtimeDependencies["kde/pim/eventviews"] = None
        self.runtimeDependencies["kde/pim/kdepim-runtime"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.defines["executable"] = r"bin\kalendar.exe"
