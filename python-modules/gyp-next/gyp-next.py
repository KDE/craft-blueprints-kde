# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "GYP can Generate Your Projects."

        # nss build fails with versions >= 0.17.0 on MSVC
        # TODO: test other platforms
        # 0.16.1 is not available on pypi, building from the tarball
        for ver in ["0.16.1"]:
            self.targets[ver] = f"https://github.com/nodejs/gyp-next/archive/refs/tags/v{ver}.zip"
            self.targetInstSrc[ver] = f"gyp-next-{ver}"
        self.defaultTarget = "0.16.1"

    def setDependencies(self):
        self.buildDependencies["python-modules/build"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.buildDependencies["python-modules/setuptools"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
