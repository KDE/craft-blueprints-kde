import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/ampl/gsl.git"
        for ver in ["2.2.1", "2.5.0", "2.7.0"]:
            self.targets[ver] = f"https://github.com/ampl/gsl/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gsl-{ver}"
            self.archiveNames[ver] = f"gsl-{ver}.tar.gz"
        self.targetDigests["2.2.1"] = (["ca58c082a925efe83a30ae4b9882511aee5937f6e6db17e43365a60e29a0a52e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.0"] = (["e030783224c32aa8e1659c8df61355f229b4ecbf09732ba46c7f4040bbd7c940"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.7.0"] = (["8a584e671931e975758d2e156c0ab7838af7cf02a984bfab5c545464615c8214"], CraftHash.HashAlgorithm.SHA256)

        self.description = "GNU Scientific Library"

        self.patchToApply["2.2.1"] = [("disable-broken-pdb-install.patch", 1)]

        self.defaultTarget = "2.7.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # AMPL not needed (avoid submodule ASL dependency)
        self.subinfo.options.configure.args += ["-DGSL_DISABLE_TESTS=ON", "-DNO_AMPL_BINDINGS=ON"]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.dynamic.buildStatic = True
