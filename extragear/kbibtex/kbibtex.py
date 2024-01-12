import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["kbibtex/0.9"] = "https://invent.kde.org/office/kbibtex.git|kbibtex/0.9"
        self.targetUpdatedRepoUrl["kbibtex/0.9"] = ("https://anongit.kde.org/kbibtex|kbibtex/0.9", "https://invent.kde.org/office/kbibtex.git|kbibtex/0.9")
        self.svnTargets["kbibtex/0.10"] = "https://invent.kde.org/office/kbibtex.git|kbibtex/0.10"
        self.targetUpdatedRepoUrl["kbibtex/0.10"] = ("https://anongit.kde.org/kbibtex|kbibtex/0.10", "https://invent.kde.org/office/kbibtex.git|kbibtex/0.10")
        self.svnTargets["master"] = "https://invent.kde.org/office/kbibtex.git|master"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/kbibtex|master", "https://invent.kde.org/office/kbibtex.git|master")
        self.defaultTarget = "master"

        self.description = "An editor for bibliographies used with LaTeX"
        self.webpage = "https://userbase.kde.org/KBibTeX"
        self.displayName = "KBibTeX"

    def setDependencies(self):
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["kde/applications/okular"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()

    def createPackage(self):
        self.defines["productname"] = "KBibTeX"
        self.defines["website"] = "https://userbase.kde.org/KBibTeX"
        self.defines["executable"] = "bin\\kbibtex.exe"
        self.defines["icon"] = os.path.join(self.blueprintDir(), "kbibtex.ico")

        return super().createPackage()
