import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KDE document viewer"
        self.displayName = "Okular"

    def setDependencies(self):
        self.buildDependencies["libs/chm"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/djvu"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/ebook-tools"] = None
        self.buildDependencies["libs/libspectre"] = None
        self.runtimeDependencies["libs/ghostscript"] = None
        self.runtimeDependencies["kde/applications/libkexiv2"] = None
        self.runtimeDependencies["kde/kdegraphics/kdegraphics-mobipocket"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kjs"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/khtml"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\okular.exe"
        self.defines["mimetypes"] = ["application/pdf"]
        self.defines["file_types"] = [".pdf"]

        # okular icons
        self.defines["icon"] = os.path.join(self.packageDir(), "okular.ico")
        self.defines["icon_png"] = os.path.join(self.packageDir(), ".assets", "150-apps-okular.png")
        self.defines["icon_png_44"] = os.path.join(self.packageDir(), ".assets", "44-apps-okular.png")

        # this requires an 310x150 variant in addition!
        #self.defines["icon_png_310x310"] = os.path.join(self.packageDir(), ".assets", "310-apps-okular.png")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        self.ignoredPackages.append("kde/frameworks/kdesignerplugin")
        self.ignoredPackages.append("kde/frameworks/kemoticons")

        return TypePackager.createPackage(self)
