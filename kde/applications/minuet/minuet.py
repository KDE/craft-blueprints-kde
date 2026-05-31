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


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.defines["shortcuts"] = [{"name": "Minuet", "target": "bin/minuet.exe", "description": self.subinfo.description}]

    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_macos.txt")
            self.addExecutableFilter(r"(bin|libexec)/(?!(minuet|minuet-bin)).*")

        return super().createPackage()

    def preArchive(self):
        if CraftCore.compiler.isMacOS:
            archiveDir = self.archiveDir()
            fluidsynthFramework = archiveDir / "Library/Frameworks/FluidSynth.framework"
            if fluidsynthFramework.exists():
                if not utils.createDir(archiveDir / "lib"):
                    return False
                if not utils.moveFile(fluidsynthFramework, archiveDir / "lib"):
                    return False

            for launcher in (
                archiveDir / "bin/minuet",
                archiveDir / "Applications/KDE/minuet.app/Contents/MacOS/minuet",
            ):
                realExecutable = launcher.with_name("minuet-bin")
                if launcher.exists() and not realExecutable.exists():
                    if not utils.moveFile(launcher, realExecutable):
                        return False
                if realExecutable.exists():
                    launcher.write_text(
                        """#!/bin/sh
unset QT_PLUGIN_PATH
unset QML_IMPORT_PATH
unset QML2_IMPORT_PATH

SELF_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
exec "$SELF_DIR/minuet-bin" "$@"
""",
                        encoding="UTF-8",
                    )
                    launcher.chmod(0o755)

        return super().preArchive()
