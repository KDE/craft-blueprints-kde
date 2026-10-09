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
        print("SDKROOT =", sdk)
        env["SDKROOT"] = sdk
        env["PYTHONPATH"] = CraftCore.standardDirs.craftRoot() / "lib/python3.11/site-packages"
        return env

    # Craft only reports the raw exit code when shiboken6 fails to start, so resolve the loader error here
    def _diagnoseShiboken(self):
        craftRoot = CraftCore.standardDirs.craftRoot()
        candidates = glob.glob(str(craftRoot / "lib/site-packages/shiboken6_generator/shiboken6.exe"))
        if not candidates:
            candidates = glob.glob(str(craftRoot / "**/shiboken6.exe"), recursive=True)
        if not candidates:
            CraftCore.log.error(f"shiboken6.exe not found below {craftRoot}")
            return

        shibokenExe = candidates[0]
        shibokenDir = os.path.dirname(shibokenExe)
        CraftCore.log.info(f"shiboken6: {shibokenExe}")
        CraftCore.log.info(f"shiboken6 directory: {sorted(os.listdir(shibokenDir))}")
        searchPath = [p for p in os.environ.get("PATH", "").split(os.pathsep) if any(k in p.lower() for k in ("clang", "llvm", "qt"))]
        CraftCore.log.info(f"PATH entries providing Qt/clang: {searchPath}")

        result = subprocess.run([shibokenExe, "--version"], capture_output=True, text=True, timeout=60)
        CraftCore.log.info(f"shiboken6 --version exit code: {result.returncode} (0x{result.returncode & 0xFFFFFFFF:08X})")
        if result.stdout.strip():
            CraftCore.log.info(f"shiboken6 stdout: {result.stdout.strip()}")
        if result.stderr.strip():
            CraftCore.log.info(f"shiboken6 stderr: {result.stderr.strip()}")
        if result.returncode == 0:
            return

        # 0xC0000135: a dependent DLL is missing, 0xC0000139: DLL found but an imported symbol is not exported
        dependents = subprocess.run(["dumpbin", "/dependents", shibokenExe], capture_output=True, text=True, shell=True)
        CraftCore.log.error(f"dumpbin /dependents:\n{dependents.stdout or dependents.stderr}")
        for line in dependents.stdout.splitlines():
            dll = line.strip()
            if not dll.lower().endswith(".dll"):
                continue
            beside = os.path.exists(os.path.join(shibokenDir, dll))
            inPath = subprocess.run(["where", dll], capture_output=True, text=True, shell=True).stdout.split()
            CraftCore.log.error(f"{dll}: besideExe={beside}, inPath={inPath or 'not found'}")

    def _checkShiboken(self):
        if not CraftCore.compiler.isWindows:
            return
        try:
            self._diagnoseShiboken()
        except Exception as e:
            CraftCore.log.error(f"shiboken6 diagnostic failed: {e}")

    def configure(self):
        self._checkShiboken()
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        self._checkShiboken()
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

            # Copy PySide6 package recursively, excluding bundled Qt DLLs
            destPyside = destSitePackages / "PySide6"
            if pysideDir.exists():
                def ignore_qt_dlls(dir, files):
                    # Skip Qt*.dll files - we use Craft's Qt from bin/
                    return [f for f in files if f.startswith("Qt") and f.endswith(".dll")]
                shutil.copytree(pysideDir, destPyside, ignore=ignore_qt_dlls, dirs_exist_ok=True)
                CraftCore.log.info("Copied PySide6 package to bin/Lib/site-packages/")

            # Copy shiboken6 package recursively
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
        print("preArchive(), archive dir:", archiveDir)

        if CraftCore.compiler.isMacOS and not CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            # Move cantor_pythonserver to the package
            defines = self.setDefaults(self.defines)
            appPath = self.getMacAppPath(defines)
            print("preArchive(), app path:", appPath)

            # Copy entitlements next to .app for signing
            entitlementsSource = self.sourceDir() / "labplot.entitlements"
            if entitlementsSource.exists():
                entitlementsDest = appPath.parent / "labplot.entitlements"
                utils.copyFile(entitlementsSource, entitlementsDest, linkOnly=False)
                CraftCore.log.info(f"Copied entitlements next to .app: {entitlementsDest}")
            else:
                CraftCore.log.warning(f"Entitlements source not found at: {entitlementsSource}")

            # if not utils.copyFile(
            #    archiveDir / "Applications/KDE/cantor_pythonserver.app/Contents/MacOS/cantor_pythonserver",
            #    appPath / "Contents/MacOS",
            #    linkOnly=False
            # ):
            #    return False

            taskLog = os.path.join(archiveDir, "Applications", "KDE", "task.log")
            if os.path.exists(taskLog):
                print("task.log:", taskLog)
                with open(taskLog, "r") as f:
                    print(f.read())
            taskDebugLog = os.path.join(archiveDir, "Applications", "KDE", "task-debug.log")
            if os.path.exists(taskDebugLog):
                print("task-debug.log:", taskDebugLog)
                with open(taskDebugLog, "r") as f:
                    print(f.read())

            pythonSitePackageLocations = glob.glob(os.path.join(CraftCore.standardDirs.craftRoot(), "lib/python*/site-packages"))
            pythonPackages = os.listdir(pythonSitePackageLocations[0])
            print("preArchive(), Python craftRoot site packages:", pythonPackages)

            pysideLocation = os.path.join(pythonSitePackageLocations[0], "PySide6")
            shibokenLocation = os.path.join(pythonSitePackageLocations[0], "shiboken6")
            print("preArchive(), PySide/shiboken craftRoot lib location:", pysideLocation, shibokenLocation)

            # copy complete site-packages fails signing
            # copy dylibs only
            utils.copyFile(os.path.join(pysideLocation, "libpyside6.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libpyside6.abi3.6.11.dylib"), linkOnly=False)
            utils.copyFile(os.path.join(pysideLocation, "libpyside6qml.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libpyside6qml.abi3.6.11.dylib"), linkOnly=False)
            utils.copyFile(os.path.join(shibokenLocation, "libshiboken6.abi3.6.11.dylib"), os.path.join(appPath, "Contents", "Frameworks", "libshiboken6.abi3.6.11.dylib"), linkOnly=False)

            pythonFrameworksPackages = os.path.join(appPath, "Contents/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")
            pysidePath = os.path.join(pythonFrameworksPackages, "PySide6")
            shibokenPath = os.path.join(pythonFrameworksPackages, "shiboken6")

            # also needed libs to frameworks site-packages
            pysideLibs = glob.glob(os.path.join(pysideLocation, "*.so"))
            os.makedirs(pysidePath, exist_ok=True)
            for lib in pysideLibs:
                utils.copyFile(lib, pysidePath, linkOnly=False)
            os.makedirs(shibokenPath, exist_ok=True)
            utils.copyFile(os.path.join(shibokenLocation, "Shiboken.abi3.so"), shibokenPath, linkOnly=False)

            utils.copyFile(os.path.join(pysideLocation, "__init__.py"), pysidePath, linkOnly=False)
            utils.copyFile(os.path.join(shibokenLocation, "__init__.py"), shibokenPath, linkOnly=False)
            # fix falsely picked up system Python lib
            # utils.system(["install_name_tool", "-change", "/Library/Frameworks/Python.framework/Versions/3.12/Python", os.path.join(appPath, "Contents", "Frameworks", "Python.framework", "Versions", "3.11", "Python"), os.path.join(appPath, "Contents", "MacOS", "cantor_pythonserver")])
            # utils.system(
            #    [
            #        "install_name_tool",
            #        "-change",
            #        "/Library/Frameworks/Python.framework/Versions/3.12/Python",
            #        "@executable_path/../Frameworks/Python.framework/Versions/3.11/Python",
            #        os.path.join(appPath, "Contents", "MacOS", "cantor_pythonserver")
            #    ]
            # )

        print("preArchive() DONE")
        return super().preArchive()
