import info
import utils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def make(self):
        env = {}
        if CraftCore.compiler.isWindows:
            # shorten the path to qsb.exe ...
            shortDevUtils = CraftShortPath(Path(CraftCore.standardDirs.craftRoot()) / "bin").shortPath
            env["PATH"] = f"{shortDevUtils}/bin;{os.environ['PATH']}"
        with utils.ScopedEnv(env):
            return super().make()
