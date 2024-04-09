import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.20.4"]:
            self.targets[ver] = f"https://gitlab.gnome.org/GNOME/libsecret/-/archive/{ver}/libsecret-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libsecret-{ver}"
        self.targetDigests["0.20.4"] = (["ca34e69b210df221ae5da6692c2cb15ef169bb4daf42e204442f24fdb0520d4b"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A GObject-based library for accessing the Secret Service API of the freedesktop.org project, a cross-desktop effort to access passwords, tokens and other types of secrets."

        self.defaultTarget = "0.20.4"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["data/docbook-xsl"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/libxslt"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Dvapi=false", "-Dgtk_doc=false", "-Dintrospection=false", "-Dmanpage=false"]
