import os
import shutil

import info
import utils
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        if self.options.dynamic.useMariaDB:
            self.setMariaDbTargets()
        else:
            self.setMySqlTargets()

    def setMariaDbTargets(self):
        baseURL = "https://mariadb.kisiek.net/"
        ver = "10.2.12"
        arch = "x64" if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64 else "32"
        self.targets[ver] = f"{baseURL}mariadb-{ver}/win{arch}-packages/mariadb-{ver}-win{arch}.zip"
        self.targetInstSrc[ver] = f"mariadb-{ver}-win{arch}"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            self.targetDigests[ver] = (["b57cc78fe79633e551d88622bfa729328268da5e7b0fa58e86e838fcc906c796"], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests[ver] = (["1e6a5640a9b9e9c290f785f232ab3f623bfc5f8736e26e8ae040c0d7dde174ae"], CraftHash.HashAlgorithm.SHA256)

        self.description = "MariaDB database server and embedded library"
        self.defaultTarget = ver

    def setMySqlTargets(self):
        baseURL = "https://dev.mysql.com/get/Downloads/MySQL-5.7/"
        ver = "5.7.18"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            arch = "x64"
            self.targetDigests["5.7.18"] = (["6a3b2d070200ae4e29f8a08aceb1c76cca9beccb037de4f5ab120d657e781353"], CraftHash.HashAlgorithm.SHA256)
        else:
            arch = "32"
        self.targets[ver] = f"{baseURL}mysql-{ver}-win{arch}.zip"
        self.targetInstSrc[ver] = f"mysql-{ver}-win{arch}"

        self.description = "MySql database server and embedded library"
        self.defaultTarget = ver

    def registerOptions(self):
        self.options.dynamic.registerOption("useMariaDB", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableStriping = True
        self.subinfo.options.package.packSources = False

    def install(self):
        libname = "mariadb" if self.subinfo.options.dynamic.useMariaDB else "mysql"
        shutil.copytree(
            self.sourceDir() / "bin",
            self.installDir() / "bin",
            ignore=shutil.ignore_patterns("*.map", "*test*", "mysqld-debug.exe", "*.pl", "debug*"),
        )
        utils.copyFile(self.sourceDir() / "lib/lib{libname}.dll", self.installDir() / "bin")
        if not self.subinfo.options.dynamic.useMariaDB:
            utils.copyFile(self.sourceDir() / f"lib/lib{libname}d.dll", self.installDir() / "bin")
        shutil.copytree(
            self.sourceDir() / "lib",
            self.installDir() / "lib",
            ignore=shutil.ignore_patterns("*.map", "debug*", f"lib{libname}.dll", f"lib{libname}.dll", f"{libname}*"),
        )
        if CraftCore.compiler.compiler.isMinGW:
            utils.createImportLibs(f"lib{libname}d", self.installDir())
            utils.createImportLibs(f"lib{libname}", self.installDir())
        shutil.copytree(self.sourceDir() / "include", self.installDir() / "include", ignore=shutil.ignore_patterns("*.def"))
        shutil.copytree(self.sourceDir() / "share", self.installDir() / "share", ignore=shutil.ignore_patterns("Makefile*"))
        return True

    def qmerge(self):
        if not super().qmerge():
            return False
        datadir = CraftStandardDirs.craftRoot() / "data"
        if self.subinfo.options.dynamic.useMariaDB:
            return utils.system(["mysql_install_db", f"--datadir={datadir}"])
        else:
            if os.path.isdir(datadir) and len(os.listdir(datadir)) != 0:
                return True
            return utils.system(["mysqld", "--console", "--initialize-insecure"])
