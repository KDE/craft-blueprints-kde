# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["libs/qt5"] = None

from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.make.args = "docs"


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)

    @property
    def QtPackages(self) -> [CraftPackageObject]:
        children = CraftDependencyPackage(CraftPackageObject.get("libs/qt5")).getDependencies(DependencyType.Runtime)
        children.remove(self.package)
        children = list(filter(lambda x: x.path.startswith("libs/qt5"), children))
        print(children)
        return children


    def make(self):
        packages = self.QtPackages
        args = self.makeOptions("docs")

        for p in packages:
            CraftCore.log.info(f"Building doc for {p.path}")
            if not (
                    #utils.system([self.makeProgram, args], cwd=p.instance.buildDir()) and
                  utils.globCopyDir(p.instance.buildDir(), self.buildDir(), [f"doc/*.qch"], linkOnly=False)):
                return False
        return super().make()


    def install(self):
        return utils.globCopyDir(self.buildDir(), self.installDir(), [f"doc/*.qch"], linkOnly=False)


