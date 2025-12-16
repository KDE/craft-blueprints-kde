# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
import utils
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings project"
        self.defaultTarget = "6.10.1"

        for ver in ["6.10.1"]:
            self.targets[ver] = f"https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-{ver}-src/pyside-setup-everywhere-src-{ver}.zip"
            self.targetInstSrc[ver] = "pyside-setup-everywhere-src-%s" % ver

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.buildDependencies["libs/qt6"] = None
        # required by shiboken6
        if CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/llvm"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        """Override default pip install with setup.py install."""
        sourceDir = self.sourceDir()
        imageDir = self.imageDir()
        # see https://doc.qt.io/qtforpython-6/building_from_source/index.html
        # options: --build-type=pyside6 (only pysde6), --macos-use-libc++, --macos-sysroot=, --shiboken-extra-include-paths=,  --standalone, --verbose
        # macOS: SDKROOT required to find type_traits and skip failing WebEngineCore and dependencies
        if CraftCore.compiler.isMacOS:
            return utils.system(
                ["SDKROOT=$(xcrun --show-sdk-path)", "PYSIDE_DISABLE_UNITY=1", "python", "setup.py", "install", f"--prefix={imageDir}", "--verbose-build", "--macos-use-libc++", "--disable-pyi", "--skip-mypy-test", "--skip-modules=WebEngineCore,WebEngineWidgets,WebEngineQuick"],
                cwd=sourceDir
            )
        else:
            return utils.system(
                ["python", "setup.py", "install", f"--prefix={imageDir}", "--verbose-build", "--disable-pyi", "--skip-mypy-test"],
                cwd=sourceDir
            )
