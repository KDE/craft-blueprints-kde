import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KDE document viewer"
        self.displayName = "Okular"

        self.patchLevel["24.02.1"] = 1
        self.patchToApply["24.02.1"] = [
            ("0001-Try-to-fix-compile-error-on-macOS.patch", 1),
        ]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtimageformats"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["qt-libs/phonon"] = None
        if not CraftCore.compiler.isMacOS and not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["qt-libs/phonon-vlc"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kimageformats"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/kdegraphics/kdegraphics-mobipocket"] = None
        if not CraftCore.compiler.isAndroid:
            self.buildDependencies["libs/chm"] = None
            self.runtimeDependencies["libs/libspectre"] = None
            self.runtimeDependencies["libs/discount"] = None
            self.runtimeDependencies["libs/djvu"] = None
            self.runtimeDependencies["libs/ebook-tools"] = None
            self.runtimeDependencies["libs/ghostscript"] = None
            self.runtimeDependencies["kde/applications/libkexiv2"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
            self.runtimeDependencies["kde/plasma/plasma-activities"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kpty"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
            self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
            self.runtimeDependencies["kde/plasma/plasma-activities"] = None

            # try to use Breeze style as Windows style has severe issues for e.g. scaling
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
            self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DOKULAR_UI=mobile", "-DANDROID_LINK_EXTRA_LIBRARIES=ON"]
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DFORCE_NOT_REQUIRED_DEPENDENCIES=LibSpectre"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_mac.txt")
        self.addExecutableFilter(r"bin/(?!(okular|update-mime-database|kioworker)).*")
        self.defines["executable"] = r"bin\okular.exe"
        self.defines["mimetypes"] = ["application/pdf"]
        self.defines["file_types"] = [".pdf", ".mobi", ".epub", ".tiff", ".djvu"]

        self.defines["alias"] = "okular"

        # okular icons
        self.defines["icon"] = self.blueprintDir() / "okular.ico"
        self.defines["icon_png"] = self.sourceDir() / "icons/150-apps-okular.png"
        self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-okular.png"

        # this requires an 310x150 variant in addition!
        # self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "ui", "data", "icons", "310-apps-okular.png")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        return super().createPackage()
