

import re

import CraftCore
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["2.3"]:
            self.targets[ver] = f"https://github.com/OlafvdSpek/ctemplate/archive/ctemplate-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ctemplate-ctemplate-{ver}"

        self.targetDigests["2.3"] = (['99e5cb6d3f8407d5b1ffef96b1d59ce3981cda3492814e5ef820684ebb782556'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.3"] = [("ctemplate-2.3-20180920.diff", 1)]
        self.description = "This library provides an easy to use and lightning fast text templating system to use with C++ programs."
        self.defaultTarget = "2.3"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += f" --disable-static --enable-shared"