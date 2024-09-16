import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ref in ["master"]:  # NOTE: there is no Qt 6 release branch, yet
            self.svnTargets[ref] = "https://invent.kde.org/office/kbibtex.git|" + ref
            self.targetUpdatedRepoUrl[ref] = ("https://anongit.kde.org/kbibtex|" + ref, "https://invent.kde.org/office/kbibtex.git|" + ref)
        self.defaultTarget = "master"

        self.description = "An editor for bibliographies used with LaTeX"
        self.webpage = "https://userbase.kde.org/KBibTeX"
        self.displayName = "KBibTeX"

    def setDependencies(self):
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON", "-DQT_MAJOR_VERSION=6"]

    def createPackage(self):
        self.defines["productname"] = "KBibTeX"
        self.defines["website"] = "https://userbase.kde.org/KBibTeX"
        self.defines["executable"] = "bin\\kbibtex.exe"
        self.defines["icon"] = self.blueprintDir() / "kbibtex.ico"

        return super().createPackage()
