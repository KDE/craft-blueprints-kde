import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.21.7"]:
            self.targets[ver] = f"https://gitlab.gnome.org/GNOME/libsecret/-/archive/{ver}/libsecret-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libsecret-{ver}"
        self.targetDigests["0.21.7"] = (["944d8a6072b6f285db40b8e9927dbe4dde81dcc7d177f84271fb167ccc297f65"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A GObject-based library for accessing the Secret Service API of the freedesktop.org project, a cross-desktop effort to access passwords, tokens and other types of secrets."

        self.defaultTarget = "0.21.7"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["data/docbook-xsl"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/libxslt"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Dvapi=false", "-Dgtk_doc=false", "-Dintrospection=false", "-Dmanpage=false", "-Dcrypto=disabled"]
