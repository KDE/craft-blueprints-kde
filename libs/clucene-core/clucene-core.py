import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/boost/boost-thread"] = "default"

    def setTargets(self):
        for ver in ['0.9.16a', '0.9.20', '0.9.21b']:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = os.path.join("clucene-core-%s" % ver, "src")

        self.patchToApply['0.9.21b'] = ("0.9.21.diff", 2)
        self.targetDigests['0.9.21b'] = '8bc505b64f82723c2dc901036cb0607500870973'

        self.targets[
            '2.3.3.4'] = "http://garr.dl.sourceforge.net/project/clucene/clucene-core-unstable/2.3/clucene-core-2.3.3.4.tar.gz"
        self.targetDigests['2.3.3.4'] = '76d6788e747e78abb5abf8eaad78d3342da5f2a4'
        self.targetInstSrc['2.3.3.4'] = "clucene-core-2.3.3.4"
        self.patchToApply['2.3.3.4'] = [('clucene-core-2.3.3.4-20120704.diff', 1)]

        self.description = "high-performance, full-featured text search engine (required for compiling strigi)"
        self.defaultTarget = '2.3.3.4'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DCLUCENE_VERSION:STRING=" + self.buildTarget
        if self.buildTarget.startswith('0.9'):
            self.subinfo.options.configure.configurePath = "src"

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return True

        if not self.buildTarget.startswith('0.9'):
            return True;

        # we have an own cmake script - copy it to the right place
        cmake_script = ""
        if self.buildTarget == '0.9.16a':
            cmake_script = os.path.join(self.packageDir(), "CMakeLists-0.9.16.txt")
        else:
            cmake_script = os.path.join(self.packageDir(), "CMakeLists-0.9.20.txt")
        cmake_dest = os.path.join(self.sourceDir(), "CMakeLists.txt")
        utils.copyFile(cmake_script, cmake_dest)
        cmake_script = os.path.join(self.packageDir(), "clucene-config.h.cmake")
        cmake_dest = os.path.join(self.sourceDir(), "Clucene", "clucene-config.h.cmake")
        utils.copyFile(cmake_script, cmake_dest)

        return True
