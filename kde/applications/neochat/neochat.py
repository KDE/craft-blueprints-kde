import os

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/network/neochat.git")

        self.displayName = "NeoChat"
        self.description = "A client for matrix, the decentralized communication protocol."

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtlocation"] = None
        self.runtimeDependencies["libs/qt/qtwebview"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kquickcharts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/prison"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["qt-libs/libquotient"] = None
        self.runtimeDependencies["libs/cmark"] = None
        self.runtimeDependencies["kde/libs/kquickimageeditor"] = None
        self.runtimeDependencies["qt-libs/qcoro"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kstatusnotifieritem"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["dev-utils/libtool"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["-DNEOCHAT_APPIMAGE=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        if CraftCore.compiler.isAndroid:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_android.txt")
        self.defines["shortcuts"] = [{"name": "NeoChat", "target": "bin/neochat.exe", "appId": "neochat", "icon": self.buildDir() / "src/NEOCHAT_ICON.ico"}]
        self.defines["icon"] = self.buildDir() / "src/NEOCHAT_ICON.ico"
        # set the icons for the appx bundle
        if os.path.exists(self.sourceDir() / "icons/150-apps-neochat.png"):
            self.defines["icon_png"] = self.sourceDir() / "icons/150-apps-neochat.png"
            self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-neochat.png"
        else:
            self.defines["icon_png"] = self.blueprintDir() / "150-apps-neochat.png"
            self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-neochat.png"
        self.addExecutableFilter(r"(bin|libexec)/(?!(neochat|update-mime-database|snoretoast)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
