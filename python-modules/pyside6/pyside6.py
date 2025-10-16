# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
import utils
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings project"
        self.defaultTarget = "6.9.3"

        for ver in ["6.9.3"]:
            self.targets[ver] = f"https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-{ver}-src/pyside-setup-everywhere-src-{ver}.zip"
            self.targetInstSrc[ver] = "pyside-setup-everywhere-src-%s" % ver

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        """Override default pip install with setup.py install."""
        src = self.sourceDir()
        # see https://doc.qt.io/qtforpython-6/building_from_source/index.html
        # only pyside6: --build-type=pyside6
        return utils.system(
            "python setup.py install --verbose-build",
            cwd=src,
        )
