import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("fluentwinui3Style", not CraftCore.compiler.platform.isAndroid)
        self.options.dynamic.registerOption("fusionStyle", not CraftCore.compiler.platform.isAndroid)
        self.options.dynamic.registerOption("imagineStyle", not CraftCore.compiler.platform.isAndroid)
        self.options.dynamic.registerOption("universalStyle", not CraftCore.compiler.platform.isAndroid)

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["6.6.0"] = 1
        self.patchLevel["6.7.0"] = 1

        # See https://codereview.qt-project.org/c/qt/qtdeclarative/+/596457
        self.patchToApply["6.8.0"] = [("e6e3da4de8fac7f52eb2591cb95a04ab413f8ace.patch", 1)]
        self.patchLevel["6.8.0"] = 1

        # https://bugreports.qt.io/browse/QTBUG-132421
        self.patchToApply["6.8.1"] = [("eff776c676b042bd75604105a3876f999b9808d5.patch", 1)]
        self.patchLevel["6.8.1"] = 1

    def setDependencies(self):
        self.buildDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None
        self.runtimeDependencies["libs/qt6/qtsvg"] = None
        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["libs/qt6/qtlanguageserver"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            f"-DFEATURE_quickcontrols2_fluentwinui3={self.subinfo.options.dynamic.fluentwinui3Style.asOnOff}",
            f"-DFEATURE_quickcontrols2_fusion={self.subinfo.options.dynamic.fusionStyle.asOnOff}",
            f"-DFEATURE_quickcontrols2_imagine={self.subinfo.options.dynamic.imagineStyle.asOnOff}",
            f"-DFEATURE_quickcontrols2_universal={self.subinfo.options.dynamic.universalStyle.asOnOff}",
        ]
        if CraftCore.compiler.platform.isWindows and self.buildType() == "Debug":
            # we use a shim pointing to the debug exe, therefor the debug infix is missing here
            self.subinfo.options.configure.args += ["-D_Python_EXECUTABLE_DEBUG=python3"]
