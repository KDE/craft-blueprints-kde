import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/sparkle-project/Sparkle.git"
        for ver in ["1.22.0"]:
            self.svnTargets[ver] = f"[git]https://github.com/sparkle-project/Sparkle.git||{ver}"
        self.description = "A software update framework for macOS"
        self.webpage = "https://sparkle-project.org"
        self.defaultTarget = '1.22.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.make.args += ["release", f"BUILDDIR={self.buildDir()}"]

    def fetch(self):
        if isinstance(self, GitSource):
            if os.path.exists(self.sourceDir()):
                utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return super().fetch()

    def make(self):
        """implements the make step for Makefile projects"""
        self.enterSourceDir() # we need to call the make file in the src dir...
        return utils.system(Arguments([self.makeProgram, self.makeOptions(self.subinfo.options.make.args)]))

    def install(self):
        self.cleanImage()
        dest = Path(self.imageDir()) / "lib"
        src = Path(self.buildDir()) / "Build/Products/Release"
        utils.createDir(dest)
        files = ["Sparkle.framework", "Sparkle.framework.dSym"]
        for f in files:
            if not utils.copyDir(src / f, dest / f):
                return False
        return True