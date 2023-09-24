import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Compiler.All

    def setTargets(self):
        self.description = "Minimalistic plugin API for video effects, plugins collection"
        self.webpage = "http://frei0r.dyne.org/"
        for ver in ["2.3.1"]:
            self.targets[ver] = f"https://github.com/dyne/frei0r/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"frei0r-{ver}"
        self.targetDigests["2.3.1"] = (["dd6dbe49ba743421d8ced07781ca09c2ac62522beec16abf1750ef6fe859ddc9"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/dyne/frei0r.git"
        self.defaultTarget = "2.3.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/cairo"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/gavl"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DWITHOUT_GAVL=1"]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/frei0r-1", self.installDir() / "plugins/frei0r-1")
        return True
