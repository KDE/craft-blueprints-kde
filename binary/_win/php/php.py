# -*- coding: utf-8 -*-
from distutils.version import StrictVersion

import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = CraftCore.cache.getNightlyVersionsFromUrl("http://windows.php.net/downloads/releases",
                                                              re.compile(r"7\.\d\.\d\d"))
        versions.sort(key=lambda v: StrictVersion(v))
        for ver in versions:
            self.targets[ver] = "http://windows.php.net/downloads/releases/php-%s-Win32-VC15-%s.zip" % (
            ver, CraftCore.compiler.architecture)
            self.targetDigestUrls[ver] = (
            "http://windows.php.net/downloads/releases/sha256sum.txt", CraftHash.HashAlgorithm.SHA256)
            self.targetInstallPath[ver] = os.path.join("dev-utils", "php")
            self.defaultTarget = ver


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        # TODO: ouch
        with open(os.path.join(self.imageDir(), "dev-utils", "php", "php.ini-development"), "rt") as ini:
            with open(os.path.join(self.imageDir(), "dev-utils", "php", "php.ini"), "wt") as out:
                ext_dir = re.compile("^;\s*extension_dir\s*=\s*\"ext\".*$")
                curl = re.compile("^;\s*extension\s*=\s*curl.*$")
                for line in ini:
                    if ext_dir.match(line):
                        line = "extension_dir = \"ext\"\n"
                    elif curl.match(line):
                        line = "extension=curl\n"
                    out.write(line)
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "php.exe"),
                                os.path.join(self.imageDir(), "dev-utils", "php", "php.exe"))
