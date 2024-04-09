# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "GYP can Generate Your Projects."
        # The version in pip is super old so install directly from release zip
        for ver in ["0.16.1"]:
            self.targets[ver] = f"https://github.com/nodejs/gyp-next/archive/refs/tags/v{ver}.zip"
            self.targetInstSrc[ver] = "gyp-next-" + ver
        self.defaultTarget = "0.16.1"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
