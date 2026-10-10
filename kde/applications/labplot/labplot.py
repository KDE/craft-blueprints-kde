# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import glob
import os
import shutil
import subprocess

import info
import utils
from Blueprints.CraftVersion import CraftVersion
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppImagePackager import AppImagePackager
from Packager.AppxPackager import AppxPackager
from Packager.NullsoftInstallerPackager import NullsoftInstallerPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A FREE, open-source and cross-platform Data Visualization and Analysis software accessible to everyone"
        self.webpage = "https://labplot.org/"
        self.displayName = "LabPlot"

        for ver in ["2.9.0"]:
            self.targets[ver] = "https://download.kde.org/stable/labplot/%s/labplot-%s.tar.xz" % (ver, ver)
        for ver in ["2.10.0", "2.10.1", "2.11.1", "2.12.0", "2.12.1"]:
            self.targets[ver] = "https://download.kde.org/stable/labplot/labplot-%s.tar.xz" % ver
        for ver in ["2.9.0", "2.10.0", "2.10.1", "2.11.1", "2.12.0", "2.12.1"]:
            self.targetInstSrc[ver] = "labplot-%s" % ver
        # beta versions
        # for ver in ["2.8.99"]:
        #    self.targets[ver] = "https://download.kde.org/stable/labplot/2.9.0/labplot-2.9.0-beta.tar.xz"
        #    self.targetInstSrc[ver] = "labplot-2.9.0-beta"

        self.patchToApply["2.9.0"] = [("labplot-2.9.0.patch", 1)]
        self.patchLevel["2.9.0"] = 1
        self.patchToApply["2.12.1"] = [("labplot-2.12.1.patch", 1)]
        self.patchLevel["2.12.1"] = 1

        self.defaultTarget = "2.12.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libzip"] = None
        self.runtimeDependencies["libs/liblz4"] = None
        # netcdf installation is broken for MSVC atm
        if not CraftCore.compiler.isMSVC() and not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/netcdf"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/hdf5"] = None
            self.runtimeDependencies["libs/orcus"] = None
            self.runtimeDependencies["libs/cfitsio"] = None
            self.runtimeDependencies["libs/libfftw"] = None

        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/expat"] = None
            self.runtimeDependencies["libs/webp"] = None

        # cross compiling Cantor fails on macOS x86_64 (CD job)
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["kde/applications/cantor"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/qt6/qtserialport"] = None
            self.runtimeDependencies["libs/qt6/qtmqtt"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["qt-libs/poppler"] = None
            self.runtimeDependencies["libs/matio"] = None
            self.runtimeDependencies["libs/discount"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/qt6/qtwebsockets"] = None
        # required on macOS currently
        self.runtimeDependencies["libs/readstat"] = None
        if self.buildTarget == "master" or self.buildTarget > CraftVersion("2.10.1"):
            self.runtimeDependencies["libs/eigen3"] = None
            # optional dep, but needs more ressources
            # self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        # needed by packager
        self.runtimeDependencies["libs/brotli"] = None
        self.runtimeDependencies["libs/boost"] = None
        self.runtimeDependencies["libs/ixion"] = None
        self.runtimeDependencies["python-modules/pyside6"] = None
        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
            self.buildDependencies["python-modules/build"] = None


class Package(CMakePackageBase):
    # Define the inimal PySide6 files needed for pylabplot runtime
    PYSIDE6_REQUIRED_PYFILES = ["__init__.py", "_config.py", "_git_pyside_version.py"]
    PYSIDE6_REQUIRED_MODULES = ["QtCore", "QtGui", "QtWidgets"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DLOCAL_DBC_PARSER=ON", "-DLOCAL_VECTOR_BLF=ON", "-DENABLE_TESTS=OFF"]
        self.subinfo.options.configure.args += [f"-DPython3_ROOT_DIR={CraftCore.standardDirs.craftRoot()}"]
        if CraftCore.compiler.isMacOS:
            # readstat fails with ninja
            self.supportsNinja = False
            # cerf.h is not found when using libcerf from ports
            self.subinfo.options.configure.args += ["-DENABLE_LIBCERF=OFF"]
            # eigen/Sparse not found in gitlab builds
            self.subinfo.options.configure.args += ["-DENABLE_EIGEN3=OFF"]
            # create missing Qt header paths for shiboken6
            for subpath in ["QtCore", "QtGui", "QtWidgets"]:
                if not os.path.exists(CraftCore.standardDirs.craftRoot() / "include" / subpath):
                    utils.createSymlink(CraftCore.standardDirs.craftRoot() / "lib" / f"{subpath}.framework" / "Versions/A/Headers", CraftCore.standardDirs.craftRoot() / "include" / subpath, targetIsDirectory=True)

        # TODO: use available versions
        self.subinfo.options.configure.args += [
            f"-DIxion_INCLUDE_DIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/ixion-0.20",
            f"-DOrcus_INCLUDE_DIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/orcus-0.20",
        ]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += f'-DCMAKE_CXX_FLAGS="-I{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/boost-1_86 -EHsc"'

    # required on macOS to find type_traits
    def _getEnv(self):
        env = {}
        if not CraftCore.compiler.isMacOS:
            return env
        sdk = subprocess.check_output(["xcrun", "--show-sdk-path"], text=True).strip()
        env["SDKROOT"] = sdk
        env["PYTHONPATH"] = CraftCore.standardDirs.craftRoot() / "lib/python3.11/site-packages"
        return env

    def configure(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().make()

    def install(self):
        with utils.ScopedEnv(self._getEnv()):
            if not super().install():
                return False

        # Windows: Bundle Python stdlib and packages for Python scripting
        # Keep everything in bin/ to match cantor_pythonserver.exe expectations
        # Structure: bin/python3.exe, bin/python311.dll, bin/Lib/, bin/DLLs/
        if CraftCore.compiler.isWindows:
            craftRoot = CraftCore.standardDirs.craftRoot()
            destBin = self.imageDir() / "bin"

            # Copy Python stdlib to bin/Lib/
            srcLib = craftRoot / "bin" / "Lib"
            destLib = destBin / "Lib"
            if srcLib.exists():
                shutil.copytree(srcLib, destLib, dirs_exist_ok=True)
                CraftCore.log.info("Copied Python stdlib to bin/Lib/")

            # Copy Python extension modules to bin/DLLs/
            srcDLLs = craftRoot / "bin" / "DLLs"
            destDLLs = destBin / "DLLs"
            if srcDLLs.exists():
                shutil.copytree(srcDLLs, destDLLs, dirs_exist_ok=True)
                CraftCore.log.info("Copied Python DLLs to bin/DLLs/")

            # Copy PySide6 and shiboken6 packages to bin/Lib/site-packages/
            sitePackages = craftRoot / "lib" / "site-packages"
            pysideDir = sitePackages / "PySide6"
            shibokenDir = sitePackages / "shiboken6"
            destSitePackages = destLib / "site-packages"

            # Copy only required PySide6 files - not the entire package
            destPyside = destSitePackages / "PySide6"
            if pysideDir.exists():
                os.makedirs(destPyside, exist_ok=True)

                # Required Python files
                for pyfile in self.PYSIDE6_REQUIRED_PYFILES:
                    src = pysideDir / pyfile
                    if src.exists():
                        shutil.copy2(src, destPyside / pyfile)

                # Required .pyd modules (Qt bindings) - only what pylabplot needs
                for mod in self.PYSIDE6_REQUIRED_MODULES:
                    for ext in [".pyd", ".pyi"]:
                        src = pysideDir / f"{mod}{ext}"
                        if src.exists():
                            shutil.copy2(src, destPyside / f"{mod}{ext}")

                # The main PySide6 runtime DLL
                src = pysideDir / "pyside6.abi3.dll"
                if src.exists():
                    shutil.copy2(src, destPyside / "pyside6.abi3.dll")

                CraftCore.log.info("Copied PySide6 (minimal) to bin/Lib/site-packages/")

            # Copy shiboken6 package (small, ~500KB)
            destShiboken = destSitePackages / "shiboken6"
            if shibokenDir.exists():
                shutil.copytree(shibokenDir, destShiboken, dirs_exist_ok=True)
                CraftCore.log.info("Copied shiboken6 package to bin/Lib/site-packages/")

            # Copy PySide6 and Shiboken ABI3 DLLs to bin/ for DLL loading at runtime
            for dll in ["pyside6.abi3.dll"]:
                src = pysideDir / dll
                if src.exists():
                    shutil.copy2(src, destBin / dll)
                    CraftCore.log.info(f"Copied {dll} to bin/")

            for dll in ["shiboken6.abi3.dll"]:
                src = shibokenDir / dll
                if src.exists():
                    shutil.copy2(src, destBin / dll)
                    CraftCore.log.info(f"Copied {dll} to bin/")

        return True

    def createPackage(self):
        self.defines["appname"] = "LabPlot"
        # org.kde.labplot.desktop for AppImage
        self.defines["desktopFile"] = "labplot"

        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        # Some plugin files break codesigning on macOS, which is picky about file names
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_mac.txt")
            self.addExecutableFilter(r"(bin|libexec)/(?!(labplot|cantor_|QtWebEngineProcess)).*")
        else:
            self.addExecutableFilter(r"(bin|libexec)/(?!(labplot|cantor_|QtWebEngineProcess|python3)).*")

        self.defines["website"] = "https://labplot.org/"
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
        self.ignoredPackages.append("libs/sdl2")
        # AppImage requires several libs
        if not CraftCore.compiler.isLinux or not isinstance(self, AppImagePackager):
            self.ignoredPackages.append("libs/aom")
            self.ignoredPackages.append("libs/dav1d")
            self.ignoredPackages.append("libs/ffmpeg")
            self.ignoredPackages.append("libs/svtav1")
            self.ignoredPackages.append("libs/x265")
            self.ignoredPackages.append("libs/qt6/qtwebengine")
            self.ignoredPackages.append("libs/qt6/qtshadertools")
            self.ignoredPackages.append("libs/llvm")
        # skip dbus for macOS and Windows, we don't use it there and it only leads to issues
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()

    def preArchive(self):
        archiveDir = self.archiveDir()

        if CraftCore.compiler.isMacOS and not CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            defines = self.setDefaults(self.defines)
            appPath = self.getMacAppPath(defines)

            # Copy entitlements next to .app for signing
            entitlementsSource = self.sourceDir() / "labplot.entitlements"
            if entitlementsSource.exists():
                entitlementsDest = appPath.parent / "labplot.entitlements"
                utils.copyFile(entitlementsSource, entitlementsDest, linkOnly=False)
                CraftCore.log.info(f"Copied entitlements next to .app: {entitlementsDest}")
            else:
                CraftCore.log.warning(f"Entitlements source not found at: {entitlementsSource}")

            pythonSitePackageLocations = glob.glob(os.path.join(CraftCore.standardDirs.craftRoot(), "lib/python*/site-packages"))
            pysideLocation = os.path.join(pythonSitePackageLocations[0], "PySide6")
            shibokenLocation = os.path.join(pythonSitePackageLocations[0], "shiboken6")

            # Copy dylibs to Frameworks
            utils.copyFile(os.path.join(pysideLocation, "libpyside6.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libpyside6.abi3.6.11.dylib"), linkOnly=False)
            utils.copyFile(os.path.join(pysideLocation, "libpyside6qml.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libpyside6qml.abi3.6.11.dylib"), linkOnly=False)
            utils.copyFile(os.path.join(shibokenLocation, "libshiboken6.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libshiboken6.abi3.6.11.dylib"), linkOnly=False)

            pythonFrameworksPackages = os.path.join(appPath, "Contents/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")
            pysidePath = os.path.join(pythonFrameworksPackages, "PySide6")
            shibokenPath = os.path.join(pythonFrameworksPackages, "shiboken6")

            # Copy only required PySide6 modules (not all *.so which includes multimedia, 3D, etc.)
            os.makedirs(pysidePath, exist_ok=True)
            for mod in self.PYSIDE6_REQUIRED_MODULES:
                soFile = os.path.join(pysideLocation, f"{mod}.abi3.so")
                if os.path.exists(soFile):
                    utils.copyFile(soFile, pysidePath, linkOnly=False)

            os.makedirs(shibokenPath, exist_ok=True)
            utils.copyFile(os.path.join(shibokenLocation, "Shiboken.abi3.so"), shibokenPath, linkOnly=False)

            # Copy required Python files
            for pyfile in self.PYSIDE6_REQUIRED_PYFILES:
                src = os.path.join(pysideLocation, pyfile)
                if os.path.exists(src):
                    utils.copyFile(src, pysidePath, linkOnly=False)
            utils.copyFile(os.path.join(shibokenLocation, "__init__.py"), shibokenPath, linkOnly=False)

        return super().preArchive()
