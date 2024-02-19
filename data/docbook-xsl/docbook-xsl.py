import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["data/docbook-dtd"] = None

    def setTargets(self):
        for ver in ["1.75.2", "1.78.0", "1.78.1"]:
            self.targets[ver] = "https://downloads.sourceforge.net/docbook/docbook-xsl-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "docbook-xsl-%s" % ver
            self.targetInstallPath[ver] = "share/xml/docbook/xsl-stylesheets"

        self.targetDigests["1.75.2"] = "cd146012c07f3c2c79c1cd927ad1faf5bee6cc74"
        self.targetDigests["1.78.0"] = "39a62791e7c1479e22d13d12a9ecbb2273d66229"
        self.targetDigests["1.78.1"] = "1d668c845bb43c65115d1a1d9542f623801cfb6f"
        self.options.package.withCompiler = False
        self.options.package.packSources = False

        self.description = "document translation defintions for docbook format"
        self.defaultTarget = "1.78.1"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def install(self):
        if not super().install():
            return False
        if OsUtils.isUnix():
            return True
        return utils.moveDir(os.path.join(self.imageDir(), "share"), os.path.join(self.imageDir(), "bin", "data")) and utils.copyFile(
            os.path.join(self.blueprintDir(), "docbook-xsl-stylesheets-1.78.1.xml"), os.path.join(self.imageDir(), "etc", "xml", "docbook-xsl-stylesheets.xml")
        )

    def postQmerge(self):
        catalog = os.path.join(CraftCore.standardDirs.craftRoot(), "etc", "xml", "catalog")
        if not os.path.isfile(catalog):
            os.makedirs(os.path.dirname(catalog), exist_ok=True)
            if not utils.system(["xmlcatalog", "--create", "--noout", catalog]):
                return False
        return utils.system(
            ["xmlcatalog", "--noout", "--add", "delegateSystem", "http://docbook.sourceforge.net/release/xsl/", "docbook-xsl-stylesheets.xml", catalog]
        )
