# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"

    def setTargets(self):
        self.description = "Flex is a tool for generating scanners: programs which recognize lexical patterns in text."
        self.svnTargets['master'] = 'https://github.com/westes/flex.git'
        for ver in ["2.6.4"]:
            self.targets[ver] = f"https://github.com/westes/flex/releases/download/v{ver}/flex-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"flex-{ver}"
        self.defaultTarget = '2.6.4'


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared"

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
