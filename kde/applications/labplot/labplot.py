import info
from Blueprints.CraftVersion import CraftVersion
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppImagePackager import AppImagePackager
from Packager.AppxPackager import AppxPackager
from Packager.NullsoftInstallerPackager import NullsoftInstallerPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A FREE, open-source and cross-platform Data Visualization and Analysis software accessible to everyone"
        self.webpage = "https://labplot.kde.org/"
        self.displayName = "LabPlot"

        for ver in ["2.9.0"]:
            self.targets[ver] = "https://download.kde.org/stable/labplot/%s/labplot-%s.tar.xz" % (ver, ver)
        for ver in ["2.10.0", "2.10.1", "2.11.1"]:
            self.targets[ver] = "https://download.kde.org/stable/labplot/labplot-%s.tar.xz" % ver
        for ver in ["2.9.0", "2.10.0", "2.10.1", "2.11.1"]:
            self.targetInstSrc[ver] = "labplot-%s" % ver
        # beta versions
        # for ver in ["2.8.99"]:
        #    self.targets[ver] = "https://download.kde.org/stable/labplot/2.9.0/labplot-2.9.0-beta.tar.xz"
        #    self.targetInstSrc[ver] = "labplot-2.9.0-beta"

        self.patchToApply["2.9.0"] = [("labplot-2.9.0.patch", 1)]
        self.patchLevel["2.9.0"] = 1

        self.defaultTarget = "2.11.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libzip"] = None
        self.runtimeDependencies["libs/hdf5"] = None
        self.runtimeDependencies["libs/netcdf"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/liborcus"] = None

        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/expat"] = None
            self.runtimeDependencies["libs/webp"] = None
        else:
            self.runtimeDependencies["libs/liblz4"] = None

        # cross compiling Cantor fails on macOS x86_64 (CD job)
        if not CraftCore.compiler.isMacOS or not CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            self.runtimeDependencies["kde/applications/cantor"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtserialport"] = None
        self.runtimeDependencies["libs/qt6/qtmqtt"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["libs/matio"] = None
        self.runtimeDependencies["libs/discount"] = None
        # required on macOS currently
        self.runtimeDependencies["libs/readstat"] = None
        if not CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/python"] = None
        if self.buildTarget == "master" or self.buildTarget > CraftVersion("2.10.1"):
            self.runtimeDependencies["libs/eigen3"] = None
            self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        # needed by packager
        self.runtimeDependencies["libs/brotli"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/boost"] = None
        if CraftCore.compiler.isLinux or CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/libixion"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DLOCAL_DBC_PARSER=ON", "-DLOCAL_VECTOR_BLF=ON"]
        if CraftCore.compiler.isMacOS:
            # readstat fails with ninja
            self.supportsNinja = False
            # cerf.h is not found when using libcerf from ports
            self.subinfo.options.configure.args += ["-DENABLE_LIBCERF=OFF"]
            # eigen/Sparse not found in gitlab builds
            self.subinfo.options.configure.args += ["-DENABLE_EIGEN3=OFF"]

    def createPackage(self):
        self.defines["appname"] = "labplot"

        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        # Some plugin files break codesigning on macOS, which is picky about file names
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_mac.txt")
        self.addExecutableFilter(r"bin/(?!(labplot|cantor_|QtWebEngineProcess)).*")

        self.defines["website"] = "https://labplot.kde.org/"
        self.defines["executable"] = "bin\\labplot.exe"
        self.defines["shortcuts"] = [{"name": "LabPlot", "target": "bin/labplot.exe", "description": self.subinfo.description, "icon": "$INSTDIR\\labplot.ico"}]
        self.defines["icon"] = self.blueprintDir() / "labplot.ico"
        self.defines["icon_png"] = self.sourceDir() / "icons/150-apps-labplot.png"
        self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-labplot.png"
        self.defines["icon_png_310"] = self.sourceDir() / "icons/310-apps-labplot.png"

        # see NullsoftInstaller.nsi and NullsoftInstallerPackager.py
        if isinstance(self, NullsoftInstallerPackager):
            # register application and .lml file type
            self.defines["registry_hook"] = (
                """WriteRegStr SHCTX "Software\\Classes\\.lml" "" "LabPlot"\n"""
                """WriteRegStr SHCTX "Software\\Classes\\LabPlot" "" "LabPlot project"\n"""
                """WriteRegStr SHCTX "Software\\Classes\\LabPlot\\DefaultIcon" "" "$INSTDIR\\bin\\data\\labplot\\application-x-labplot.ico"\n"""
                """WriteRegStr SHCTX "Software\\Classes\\LabPlot\\shell" "" "open"\n"""
                """WriteRegStr SHCTX "Software\\Classes\\LabPlot\\shell\\open\\command" "" '"$INSTDIR\\bin\\labplot.exe" "%1"'\n"""
            )

            # remove old version if exists
            self.defines[
                "preInstallHook"
            ] = r"""
                Exec "$INSTDIR\unins000.exe"
                """

            # add option for desktop shortcut (see kdeconnect-kde.py) and update file associations
            # SHChangeNotify(SHCNE_ASSOCCHANGED,SHCNF_FLUSH,0,0)
            # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0, SHCNF_FLUSH = 0x1000, SHCNF_FLUSHNOWAIT = 0x2000
            self.defines[
                "sections"
            ] = r"""
                Section "Desktop Shortcut"
                        CreateShortCut "$DESKTOP\\@{productname}.lnk" "$INSTDIR\\bin\\@{appname}.exe"
                SectionEnd
                Section "Update new .lml file type"
                        System::Call "shell32::SHChangeNotify(i,i,i,i) (0x08000000, 0x1000, 0, 0)"
                SectionEnd
                """
            self.defines[
                "un_sections"
            ] = r"""
                Section "Un.Remove Shortcuts"
                    Delete "$DESKTOP\\@{productname}.lnk"
                SectionEnd
                """

        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "LabPlot"
        else:
            self.defines["mimetypes"] = ["application/x-labplot"]
        self.defines["file_types"] = [".lml"]

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("binary/r-base")
        self.ignoredPackages.append("libs/llvm")
        self.ignoredPackages.append("libs/python")
        self.ignoredPackages.append("libs/qt6/qtshadertools")
        self.ignoredPackages.append("libs/qt6/qtwebengine")
        self.ignoredPackages.append("libs/sdl2")
        # AppImage requires several libs
        if not CraftCore.compiler.isLinux or not isinstance(self, AppImagePackager):
            self.ignoredPackages.append("libs/aom")
            self.ignoredPackages.append("libs/dav1d")
            self.ignoredPackages.append("libs/ffmpeg")
            self.ignoredPackages.append("libs/svtav1")
            self.ignoredPackages.append("libs/x265")
        # skip dbus for macOS and Windows, we don't use it there and it only leads to issues
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
