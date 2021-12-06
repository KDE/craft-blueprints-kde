import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.4.0']:
            self.targets[ver] = f"https://downloads.sourceforge.net/gmerlin/gavl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gavl-{ver}"
        self.targetDigests['1.4.0'] = (['51aaac41391a915bd9bad07710957424b046410a276e7deaff24a870929d33ce'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['1.4.0'] = ('FixCputest.patch', 1)
        for ver in ['r6283']:
            self.targets[ver] = f"https://sourceforge.net/code-snapshots/svn/g/gm/gmerlin/code/gmerlin-code-{ver}-trunk-gavl.zip"
            self.targetInstSrc[ver] = f"gmerlin-code-{ver}-trunk-gavl"
        self.targetDigests['r6283'] = (['589b44f12274c5febf766891f17d68eb0d7d866f5eb4066a6775a688bff4bce4'], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMacOS:
            self.patchToApply['r6283'] = ('FixMacOS.patch', 1)

        self.description = "Low level library, upon which multimedia APIs can be built"
        self.webpage = "https://gmerlin.sourceforge.net"
        self.defaultTarget = 'r6283'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.buildTarget in ['r6283']:
            self.runtimeDependencies["libs/gnutls"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ' --without-doxygen --disable-libpng'
