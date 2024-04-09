import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.45"]:
            self.targets[ver] = f"https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-{ver}.tgz"
            self.targetInstSrc[ver] = f"openldap-{ver}"

        self.patchToApply["2.4.45"] = [
            ("openldap-2.4.45-20231209.diff", 1)
        ]  # https://gitweb.gentoo.org/repo/gentoo.git/tree/net-nds/openldap/openldap-2.4.59-r2.ebuild#n380
        if CraftCore.compiler.isWindows:
            self.patchToApply["2.4.45"] += [("openldap-2.4.45-20170628.diff", 1)]
        self.targetDigests["2.4.45"] = (["cdd6cffdebcd95161a73305ec13fc7a78e9707b46ca9f84fb897cd5626df3824"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.16"] = (["546ba591822e8bb0e467d40c4d4a30f89d937c3a507fe83a578f582f6a211327"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.6.6"] = (["082e998cf542984d43634442dbe11da860759e510907152ea579bdc42fe39ea0"], CraftHash.HashAlgorithm.SHA256)

        self.description = "an open source implementation of the Lightweight Directory Access Protocol"

        self.defaultTarget = "2.4.45"

    def setDependencies(self):
        if not CraftCore.compiler.isWindows:
            self.buildDependencies["libs/groff"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/cyrus-sasl"] = None
        self.runtimeDependencies["libs/pcre"] = None
        self.runtimeDependencies["libs/openssl"] = None


from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

if CraftCore.compiler.isWindows:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.args += ["--without-cyrus_sasl", "--disable-bdb", "--disable-hdb"]
