import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # https://codereview.qt-project.org/c/qt/qtlocation/+/604697
        self.patchToApply["6.8.0"] = [("qtlocation-stuck-tile-provider-fix.diff", 1)]
        self.patchLevel["6.8.0"] = 1
        self.patchToApply["6.8.1"] = [("qtlocation-stuck-tile-provider-fix.diff", 1)]
        # Qt's HTTP2 implementation in Qt 6.9.1 doesn't play well with the OSM tile server
        # (or their CDN), ie. tile download only works with HTTP1
        self.patchToApply["6.9.1"] = [("disable-http2-tile-fetching.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
