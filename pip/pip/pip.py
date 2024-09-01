import shutil

import info
import options
from BuildSystem.BuildSystemBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import *
from Packager.PackagerBase import *
from Source.MultiSource import *
from utils import ScopedEnv


class PipNewBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "pip")
        self.python3 = True

        self.pipPackageName = self.package.name

    def _getPython3(self):
        craftPython = CraftPackageObject.get("libs/python")
        suffix = "_d" if CraftCore.compiler.isWindows and craftPython.instance.subinfo.options.dynamic.buildType == "Debug" else ""
        # if CraftPackageObject.get("python-modules/virtualenv").isInstalled:
        #     if CraftCore.compiler.isWindows:
        #         return Path(CraftCore.standardDirs.craftRoot()) / f"etc/virtualenv/3/Scripts/python{suffix}"
        #     else:
        #         return Path(CraftCore.standardDirs.craftRoot()) / f"etc/virtualenv/3/bin/python3"

        if craftPython.isInstalled:
            python = CraftCore.standardDirs.craftRoot() / f"bin/python{suffix}{CraftCore.compiler.executableSuffix}"
            if python.exists():
                return python
            python = CraftCore.standardDirs.craftRoot() / f"bin/python3{suffix}{CraftCore.compiler.executableSuffix}"
            if python.exists():
                return python
        raise Exception("Please install libs/python first")

    @property
    def _pythons(self):
        pythons = []
        pythons.append(("3", self._getPython3()))
        print(pythons)
        return pythons

    #
    # def venvDir(self, ver):
    #     return Path(CraftCore.standardDirs.etcDir()) / "virtualenv" / ver

    def make(self):
        if self.subinfo.svnTarget():
            for ver, python in self._pythons:
                if not utils.system([python, "setup.py", "sdist"], cwd=self.sourceDir()):
                    return False
        return True

    def install(self):
        env = {}
        if CraftCore.compiler.isMSVC():
            env.update(
                {
                    "LIB": f"{os.environ['LIB']};{CraftStandardDirs.craftRoot() / 'lib'}",
                    "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include'}",
                }
            )
        with ScopedEnv(env):
            ok = True
            for ver, python in self._pythons:
                command = [
                    python,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "--upgrade-strategy",
                    "only-if-needed",
                ]
                # if not self.venvDir(ver).exists():
                command += ["--user"]
                if self.subinfo.svnTarget():
                    command += ["-e", self.sourceDir()]
                elif self.subinfo.hasTarget():
                    command += ["-e", self.sourceDir()]
                else:
                    if self.buildTarget in {"master", "latest"}:
                        command += [self.pipPackageName]
                    else:
                        command += [f"{self.pipPackageName}=={self.buildTarget}"]
                ok = ok and utils.system(command)
            return ok

    def runTest(self):
        return False


class PipNewPackageBase(PackageBase, MultiSource, PipNewBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("PipNewPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        PipNewBuildSystem.__init__(self, **kwargs)
        PackagerBase.__init__(self, **kwargs)

    def fetch(self):
        if self._sourceClass:
            return self._sourceClass.fetch(self)
        return True

    def unpack(self):
        if self._sourceClass:
            return self._sourceClass.unpack(self)
        return True

    def sourceRevision(self):
        if self._sourceClass:
            return self._sourceClass.sourceRevision(self)
        return ""

    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True


import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API."
        self.defaultTarget = "master"


class Package(PipNewPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
