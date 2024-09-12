import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isIOS:
            self.subinfo.options.configure.args += ["-DQT_NO_APPLE_SDK_AND_XCODE_CHECK=ON"]
        # Updating this always needs a corresponding change to the host tools in the CI image!
        if CraftCore.compiler.isAndroid:
            self.subinfo.defaultTarget = "6.7.2"
