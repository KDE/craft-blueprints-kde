# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["5.7.8"] = "https://www.aquamaniac.de/sites/download/download.php?package=03&release=217&file=02&dummy=aqbanking-5.7.8.tar.gz"
        self.targetDigests["5.7.8"] = (['16f86e4cc49a9eaaa8dfe3206607e627873208bce45a70030c3caea9b5afc768'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["5.7.8"] = "aqbanking-5.7.8.tar.gz"
        self.targetInstSrc["5.7.8"] = "aqbanking-5.7.8"

        self.defaultTarget = "5.7.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/ktoblzcheck"] = "default"
        self.runtimeDependencies["libs/gwenhywfar"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = "default"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        # this prevents "cannot find the library libaqhbci.la or unhandled argument libaqhbci.la"
        self.subinfo.options.make.supportsMultijob = False

    def install(self):
        if OsUtils.isWin():
            cmakes = [ os.path.join(self.buildDir(), "aqbanking-config.cmake") ]
            for cmake in cmakes:
                f = open(cmake, "r+")
                cmakeFileContents = f.readlines()
                for i in range(len(cmakeFileContents)):
                    m = re.search('set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group('root'), CraftStandardDirs.craftRoot()[:-1])

                    m2 = re.search("libaqbanking.so", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libaqbanking.so", "bin/libaqbanking-35.dll")

                f.seek(0)
                f.write(''.join(cmakeFileContents))
                f.close()
        return AutoToolsPackageBase.install(self)
