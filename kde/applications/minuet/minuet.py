import plistlib

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A KDE Software for Music Education."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt/qtquickeffects"] = "default"
        self.runtimeDependencies["libs/fluidsynth"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None
        else:
            self.runtimeDependencies["libs/glib"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            if CraftCore.compiler.isMacOS:
                self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
                self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        icon = self.sourceDir() / "src/app/icons/minuet.ico"
        self.defines["icon"] = icon
        self.defines["nsis_include"] = f'!define MUI_UNICON "{icon}"'
        self.defines["shortcuts"] = [{"name": "Minuet", "target": "bin/minuet.exe", "description": self.subinfo.description}]
        self.defines["icon_png"] = self.sourceDir() / "src/app/icons/150-apps-minuet.png"
        self.defines["icon_png_44"] = self.sourceDir() / "src/app/icons/44-apps-minuet.png"

    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_macos.txt")
            self.addExecutableFilter(r"(bin|libexec)/(?!minuet).*")
        elif CraftCore.compiler.isWindows:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_windows.txt")

        return super().createPackage()

    @staticmethod
    def _macosLocaleName(locale):
        if locale == "ca@valencia":
            return "ca-ES-valencia"

        normalized = locale.replace("_", "-")
        if "@" in normalized:
            language, modifier = normalized.split("@", 1)
            normalized = f"{language}-{modifier}"
        return normalized

    def _minuetLocalizations(self, localeDir):
        if not localeDir.exists():
            return []

        localizations = set()
        for catalog in localeDir.glob("*/LC_MESSAGES/minuet.mo"):
            locale = catalog.parents[1].name
            localizations.add(self._macosLocaleName(locale))
        return sorted(localizations)

    def _updateMacOSLocalizations(self, archiveDir):
        localizations = self._minuetLocalizations(archiveDir / "share/locale")
        if not localizations:
            CraftCore.log.warning("No Minuet translations found; macOS app language selection will only expose the development region.")
            return True

        plistPath = archiveDir / "Applications/KDE/minuet.app/Contents/Info.plist"
        if not plistPath.exists():
            CraftCore.log.error(f"Unable to update macOS localizations; Info.plist does not exist: {plistPath}")
            return False

        with plistPath.open("rb") as plistFile:
            plist = plistlib.load(plistFile)

        plist["CFBundleIdentifier"] = "org.kde.minuet"
        plist["CFBundleName"] = "Minuet"
        plist["CFBundleDevelopmentRegion"] = "en"
        plist["CFBundleLocalizations"] = localizations

        with plistPath.open("wb") as plistFile:
            plistlib.dump(plist, plistFile)

        CraftCore.log.info(f"Advertised {len(localizations)} Minuet localizations in the macOS bundle.")
        return True

    def preArchive(self):
        if CraftCore.compiler.isMacOS:
            archiveDir = self.archiveDir()
            if not self._updateMacOSLocalizations(archiveDir):
                return False

            fluidsynthFramework = archiveDir / "Library/Frameworks/FluidSynth.framework"
            if fluidsynthFramework.exists():
                if not utils.createDir(archiveDir / "lib"):
                    return False
                if not utils.moveFile(fluidsynthFramework, archiveDir / "lib"):
                    return False

        return super().preArchive()
