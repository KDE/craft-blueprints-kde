import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # https://raw.githubusercontent.com/microsoft/vcpkg/a618637937298060bdbe5fbcfb628eabd1082c8a/ports/qtimageformats/no_target_promotion_latest.patch
        self.patchToApply["6.4.3"] = [("qtimageformats-6.4.3-20230517.diff", 1)]
        self.patchLevel["6.4.3"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/webp"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DFEATURE_jasper=OFF"]
