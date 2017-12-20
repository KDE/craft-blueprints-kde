import info


class subinfo(info.infoclass):
    def setTargets( self ):

        for ver in ["0.7.4"]:
            self.targets[ver] = f"http://downloads.sourceforge.net/libdmtx/libdmtx-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libdmtx-{ver}"

        self.targetDigests["0.7.4"] = (['b62c586ac4fad393024dadcc48da8081b4f7d317aa392f9245c5335f0ee8dd76'], CraftHash.HashAlgorithm.SHA256)

        #self.patchToApply["1.9.0"] = [("gpgme-1.9.0-20170801.diff", 1)]

        self.shortDescription = "libdmtx is open source software for reading and writing Data Matrix barcodes on Linux, Unix, OS X, Windows, and mobile devices. At its core libdmtx is a native shared library, allowing C/C++ programs to use its capabilities without extra restrictions or overhead."
        self.defaultTarget = "0.7.4"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args = "--enable-static=no --enable-shared=yes"


    def make(self):
        if not AutoToolsPackageBase.make(self):
            return False
        return self.shell.execute(os.path.join(self.buildDir(), ".libs"), CraftCore.cache.findApplication("gcc"), "-shared -o dmtx.dll libdmtx_la-dmtx.o -Wl,--out-implib,libdmtx.dll.a")

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        utils.copyFile(os.path.join(self.buildDir(), ".libs", "dmtx.dll"), os.path.join(self.installDir(), "bin", "dmtx.dll"), linkOnly=False)
        utils.copyFile(os.path.join(self.buildDir(), ".libs", "libdmtx.dll.a"), os.path.join(self.installDir(), "lib", "libdmtx.dll.a"), linkOnly=False)
        return self.copyToMsvcImportLib()
