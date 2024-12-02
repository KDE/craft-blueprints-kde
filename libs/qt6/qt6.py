from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.platform.isIOS:
            self.subinfo.options.configure.args += ["-DQT_NO_APPLE_SDK_AND_XCODE_CHECK=ON"]
        # Updating this always needs a corresponding change to the host tools in the CI image!
        if CraftCore.compiler.platform.isAndroid:
            self.subinfo.defaultTarget = "6.8.1"
        elif CraftCore.compiler.platform.isWindows:
            self.subinfo.options.configure.args += ["-DQT_GENERATE_SBOM=OFF"]
