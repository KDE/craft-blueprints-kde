import os

import info
import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["4.2", "4.5"]:
            self.targets[ver] = f"https://www.docbook.org/xml/{ver}/docbook-xml-{ver}.zip"
            self.targetInstallPath[ver] = f"share/xml/docbook/schema/dtd/{ver}"
        for ver in ["5.0"]:
            self.targets[ver] = f"https://www.docbook.org/xml/{ver}/docbook-{ver}.zip"
            self.targetInstallPath[ver] = f"share/xml/docbook/schema/dtd/{ver}"
        self.targetDigests["4.2"] = "5e3a35663cd028c5c5fbb959c3858fec2d7f8b9e"
        self.targetDigests["4.5"] = "b9124233b50668fb508773aa2b3ebc631d7c1620"
        self.targetDigests["5.0"] = "49f274e67efdee771300cba4da1f3e4bc00be1ec"

        self.description = "document type definition for docbook format"
        # note: use the version specified as DOCBOOKXML_CURRENTDTD_VERSION in
        #       FindDocBookXML.cmake of kdelibs or install all DTDs at the same time
        self.defaultTarget = "4.5"


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def install(self):
        if not super().install():
            return False
        if OsUtils.isUnix():
            return True
        return utils.moveDir(self.imageDir() / "share", self.imageDir() / "bin/data") and utils.copyFile(
            self.blueprintDir() / "docbook-dtd-4.2.xml", self.imageDir() / "etc/xml/docbook-dtd-4.5.xml"
        )

    def postQmerge(self):
        catalog = CraftCore.standardDirs.craftRoot() / "etc/xml/catalog"
        if not os.path.isfile(catalog):
            os.makedirs(os.path.dirname(catalog), exist_ok=True)
            if not utils.system(["xmlcatalog", "--create", "--noout", catalog]):
                return False
        return utils.system(["xmlcatalog", "--noout", "--add", "nextCatalog", "", "docbook-dtd-4.5.xml", catalog])
