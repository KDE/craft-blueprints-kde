# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "html5lib is a pure-python library for parsing HTML. It is designed to conform to the WHATWG HTML specification, as is implemented by all major web browsers"

        for ver in ["1.1"]:
            self.targets[ver] = f"https://github.com/html5lib/html5lib-python/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"html5lib-python-{ver}"

        self.targetDigests["1.1"] = (["66e9e24a53c10c27abb6be8a3cf2cf55824c6ea1cef8570a633cb223ec46e894"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.1"] = [
            # https://github.com/html5lib/html5lib-python/pull/589
            ("589.patch", 1),
            # https://github.com/html5lib/html5lib-python/pull/594
            ("594.patch", 1),
        ]

        self.svnTargets["master"] = ""
        self.defaultTarget = "1.1"

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["python-modules/six"] = None
        self.runtimeDependencies["python-modules/webencodings"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
