import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Updating this always needs a corresponding change to the host tools in the CI image!
        if CraftCore.compiler.isAndroid:
            self.subinfo.defaultTarget = "6.8.0"
