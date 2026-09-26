# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

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

        self.patchToApply["6.11.2"] = [
            ("shiboken-include-pep384impl.patch", 1),
            ("python-libdir-fallback.patch", 1),
            ("skip-plugins.patch", 1),
            ("skip-designer-copy.patch", 1)
        ]
        self.patchLevel["6.11.2"] = 2

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtremoteobjects"] = None
        # required by shiboken6
        self.buildDependencies["libs/llvm"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        """Build PySide6 from source."""
        sourceDir = self.sourceDir()
        env = {}
        if CraftCore.compiler.isWindows:
            env["LLVM_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())
            env["CLANG_INSTALL_DIR"] = str(CraftStandardDirs.craftRoot())

        with utils.ScopedEnv(env):
            if CraftCore.compiler.isMacOS:
                return utils.system(
                    f"SDKROOT=$(xcrun --show-sdk-path) PYSIDE_DISABLE_UNITY=1 python setup.py build --verbose-build --macos-use-libc++ --disable-pyi --skip-modules=WebEngineCore,WebEngineWidgets,WebEngineQuick",
                    cwd=sourceDir
                )
            else:
                # Skip QML/Designer modules: QML directory copy fails with escaping errors on Windows
                # Skip WebEngine modules: require Chromium dependencies not available in Craft
                return utils.system(
                    ["python", "setup.py", "build",
                     "--limited-api=yes",
                     "--disable-pyi",
                     "--skip-modules=Designer,Positioning,WebEngineCore,WebEngineWidgets,WebEngineQuick,WebChannel,Quick,Qml,QuickControls2,QuickTest,QuickWidgets,UiTools"],
                    cwd=sourceDir
                )

    def install(self):
        """Install PySide6 without rebuilding."""
        import shutil
        import glob
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
                # --skip-build: prevents setup.py from rebuilding (which would recreate qml dir)
                # --skip-modules: must match make() to prevent module mismatch errors
                return utils.system(
                    ["python", "setup.py", "install",
                     f"--prefix={imageDir}",
                     "--skip-build",
                     "--skip-mypy-test",
                     "--skip-modules=Designer,Positioning,WebEngineCore,WebEngineWidgets,WebEngineQuick,WebChannel,Quick,Qml,QuickControls2,QuickTest,QuickWidgets,UiTools"],
                    cwd=sourceDir
                )
