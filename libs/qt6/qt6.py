import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isAndroid:
            self.subinfo.defaultTarget = "6.7.0"
