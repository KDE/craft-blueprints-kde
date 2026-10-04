# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import glob
import shutil
import subprocess

import info
import utils
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings project"
        self.defaultTarget = "6.11.2"

        for ver in ["6.10.1", "6.10.3", "6.11.0", "6.11.2"]:
            self.targets[ver] = f"https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-{ver}-src/pyside-setup-everywhere-src-{ver}.zip"
            self.targetInstSrc[ver] = "pyside-setup-everywhere-src-%s" % ver

        if CraftCore.compiler.isWindows:
            self.patchToApply["6.11.2"] = [
                ("shiboken-include-pep384impl.patch", 1),
                ("python-libdir-fallback.patch", 1),
                ("skip-plugins.patch", 1),
                ("skip-designer-copy.patch", 1)
            ]
            self.patchLevel["6.11.2"] = 4

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtremoteobjects"] = None
        # required by shiboken6, its libclang is bundled into the package by _bundleLibclang()
        self.buildDependencies["libs/llvm"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        """Build PySide6 from source."""
        # Windows: Python headers contain #pragma comment(lib, "python3XX.lib") which
        # forces the linker to require the versioned lib even when CMake links python3.lib.
        # Craft builds Python with stable ABI (python3.lib only), so create python3XX.lib
        # as a copy to satisfy the #pragma directive.
        if CraftCore.compiler.isWindows:
            lib_dir = CraftStandardDirs.craftRoot() / "lib"
            python3_lib = lib_dir / "python3.lib"
            if python3_lib.exists():
                # Query Craft's Python for its version (not sys.version_info which is Craft's runner)
                python_exe = CraftStandardDirs.craftRoot() / "bin" / "python.exe"
                try:
                    result = subprocess.run(
                        [str(python_exe), "-c", "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')"],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        pythonXY_lib = lib_dir / f"python{version}.lib"
                        if not pythonXY_lib.exists():
                            CraftCore.log.info(f"Creating {pythonXY_lib} from {python3_lib} for #pragma compatibility")
                            shutil.copy2(python3_lib, pythonXY_lib)
                except Exception as e:
                    CraftCore.log.warning(f"Could not determine Python version: {e}")

        sourceDir = self.sourceDir()
        env = {}
        if CraftCore.compiler.isWindows:
            env["LLVM_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())
            env["CLANG_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())

        with utils.ScopedEnv(env):
            if CraftCore.compiler.isMacOS:
                return utils.system(
                    "SDKROOT=$(xcrun --show-sdk-path) PYSIDE_DISABLE_UNITY=1 python setup.py build --verbose-build --macos-use-libc++ --disable-pyi --skip-modules=WebEngineCore,WebEngineWidgets,WebEngineQuick",
                    cwd=sourceDir
                )
            else:
                # Skip QML/Designer modules: QML directory copy fails with escaping errors on Windows
                # Skip WebEngine modules: require Chromium dependencies not available in Craft
                return utils.system(
                    ["python", "setup.py", "build",
                     "--limited-api=yes",
                     "--disable-pyi",
                     "--skip-modules=Designer,Positioning,Location,WebEngineCore,WebEngineWidgets,WebEngineQuick,WebChannel,WebView,Qml,Quick,Quick3D,QuickControls2,QuickTest,QuickWidgets,UiTools,Graphs,GraphsWidgets"],
                    cwd=sourceDir
                )

    # dev-utils/bin/libclang.dll precedes bin/ in PATH, so ship the libclang shiboken6 was linked against next to it
    def _bundleLibclang(self):
        if not CraftCore.compiler.isWindows:
            return True
        libclang = CraftStandardDirs.craftRoot() / "bin/libclang.dll"
        target = self.imageDir() / "lib/site-packages/shiboken6_generator"
        if not libclang.exists() or not target.is_dir():
            CraftCore.log.error(f"cannot bundle libclang: {libclang} exists={libclang.exists()}, {target} exists={target.is_dir()}")
            return False
        return utils.copyFile(libclang, target / "libclang.dll", linkOnly=False)

    def install(self):
        """Install PySide6 without rebuilding."""
        sourceDir = self.sourceDir()
        imageDir = self.imageDir()
        env = {}
        if CraftCore.compiler.isWindows:
            env["LLVM_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())
            env["CLANG_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())

        # Windows: Delete qml directory before install to prevent copy escaping error
        # The directory is empty (QML modules skipped) but copy still fails with backslash escaping bug
        qml_dirs = glob.glob(str(sourceDir / "build" / "*" / "package" / "PySide6" / "qml"))
        for qml_dir in qml_dirs:
            shutil.rmtree(qml_dir)

        # See https://doc.qt.io/qtforpython-6/building_from_source/index.html
        # macOS: SDKROOT required to find type_traits and skip failing WebEngineCore and dependencies
        with utils.ScopedEnv(env):
            if CraftCore.compiler.isMacOS:
                return utils.system(
                    f"SDKROOT=$(xcrun --show-sdk-path) PYSIDE_DISABLE_UNITY=1 python setup.py install --prefix={imageDir} --verbose-build --macos-use-libc++ --disable-pyi --skip-mypy-test --skip-modules=WebEngineCore,WebEngineWidgets,WebEngineQuick",
                    cwd=sourceDir
                )
            else:
                # disabled (prevents installation of header,typesystem, etc.): --skip-build: prevents setup.py from rebuilding (which would recreate qml dir)
                # --skip-modules: must match make() to prevent module mismatch errors
                if not utils.system(
                    ["python", "setup.py", "install",
                     f"--prefix={imageDir}",
                     "--skip-mypy-test",
                     "--skip-modules=Designer,Positioning,Location,WebEngineCore,WebEngineWidgets,WebEngineQuick,WebChannel,WebView,Qml,Quick,Quick3D,QuickControls2,QuickTest,QuickWidgets,UiTools,Graphs,GraphsWidgets"],
                    cwd=sourceDir
                ):
                    return False
                return self._bundleLibclang()
