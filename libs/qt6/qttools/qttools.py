import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/llvm"] = None
        self.patchToApply["6.4.0"] = [("fix-build-clang15.diff", 1)]
        self.patchToApply["6.4.0"] += [("fix-build-clang16.diff", 1)]
        self.patchLevel["6.4.0"] = 1


from Package.CMakePackageBase import *


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isMSVC() and self.buildType() == "Debug":
            self.subinfo.options.configure.args += ["-DQT_FEATURE_clangcpp=OFF"]
