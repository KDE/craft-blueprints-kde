import info

from Package.MSBuildPackageBase import *
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets( self ):
        for ver in ["1.9"]:
            self.targets[ver] = f"https://github.com/breakfastquay/rubberband/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rubberband-{ver}"
            self.patchToApply[ver] = ("fftw3-linking.patch", 0)
        self.targetDigests["1.9"] = (['779e9a5e45f869618261b98b8d0c262fcbe066418a1c836fb85de47fbc1b29aa'], CraftHash.HashAlgorithm.SHA256)
        self.description = "An audio time-stretching and pitch-shifting library and utility program"
        self.webpage = "http://breakfastquay.com/rubberband/"
        self.patchLevel["1.9"] = 1
        self.defaultTarget = "1.9"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/libsndfile"] = None

class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["--disable-programs", "--disable-vamp", "--disable-ladspa"]

class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "rubberband.sln")
        self.msbuildTargets = ["rubberband-dll"]

    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False):
            return True
        return utils.copyDir(self.sourceDir() /  "rubberband", self.installDir() / "include/rubberband")

if CraftCore.compiler.isGCCLike():
    class Package(PackageAutoTools):
        def __init__(self):
            PackageAutoTools.__init__(self)
            self.subinfo.options.useShadowBuild = False

else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
