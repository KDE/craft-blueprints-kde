import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["4.2", "4.5"]:
            self.targets[ver] = "http://www.docbook.org/xml/" + ver + "/docbook-xml-" + ver + ".zip"
            self.targetInstallPath[ver] = "share/xml/docbook/schema/dtd/%s" % ver
        for ver in ["5.0"]:
            self.targets[ver] = "http://www.docbook.org/xml/" + ver + "/docbook-" + ver + ".zip"
            self.targetInstallPath[ver] = "share/xml/docbook/schema/dtd/%s" % ver
        self.targetDigests["4.2"] = "5e3a35663cd028c5c5fbb959c3858fec2d7f8b9e"
        self.targetDigests["4.5"] = "b9124233b50668fb508773aa2b3ebc631d7c1620"
        self.targetDigests["5.0"] = "49f274e67efdee771300cba4da1f3e4bc00be1ec"

        self.description = "document type definition for docbook format"
        # note: use the version specified as DOCBOOKXML_CURRENTDTD_VERSION in
        #       FindDocBookXML.cmake of kdelibs or install all DTDs at the same time
        self.defaultTarget = "4.5"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if OsUtils.isUnix():
            return True
        return utils.moveDir(os.path.join(self.imageDir(), "share"), os.path.join(self.imageDir(), "bin", "data")) and utils.copyFile(
            os.path.join(self.blueprintDir(), "docbook-dtd-4.2.xml"), os.path.join(self.imageDir(), "etc", "xml", "docbook-dtd-4.5.xml")
        )

    def postQmerge(self):
        catalog = os.path.join(CraftCore.standardDirs.craftRoot(), "etc", "xml", "catalog")
        if not os.path.isfile(catalog):
            os.makedirs(os.path.dirname(catalog), exist_ok=True)
            if not utils.system(["xmlcatalog", "--create", "--noout", catalog]):
                return False
        return utils.system(["xmlcatalog", "--noout", "--add", "nextCatalog", "", "docbook-dtd-4.5.xml", catalog])
