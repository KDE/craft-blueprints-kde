# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "html5lib is a pure-python library for parsing HTML. It is designed to conform to the WHATWG HTML specification, as is implemented by all major web browsers"
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
