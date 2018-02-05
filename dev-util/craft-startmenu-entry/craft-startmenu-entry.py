import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1"] = f""
        self.defaultTarget = "1"

    def setDependencies(self):
        self.buildDependencies["python-modules/pywin32"] = "default"

from Package.BinaryPackageBase import *


class WinPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

        name = f"Craft {os.path.basename(CraftCore.standardDirs.craftRoot())}"
        startmenu = os.path.join(os.environ['APPDATA'], "Microsoft", "Windows", "Start Menu", "Programs", "Craft")
        self.shortCutPath = f"{os.path.join(startmenu, name)}.lnk"
        print(self.shortCutPath)
        
        
    def qmerge(self):
        import win32com.client
        root = OsUtils.toNativePath(os.path.join(CraftCore.standardDirs.craftBin(), ".."))
        powershell = CraftCore.cache.findApplication("powershell")
        icon = os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico")
        arguments = "-NoExit .\craftenv.ps1"
        os.makedirs(os.path.dirname(self.shortCutPath), exist_ok=True)
        ws = win32com.client.Dispatch("wscript.shell")
        shortcut = ws.CreateShortcut(self.shortCutPath)
        shortcut.TargetPath = powershell
        shortcut.Arguments = arguments
        shortcut.IconLocation = icon
        shortcut.WorkingDirectory = root
        shortcut.Description = f"Craft installerd to: {os.path.dirname(root)}"
        shortcut.Save()
        return super().qmerge()

    def unmerge(self):
        if os.path.exists(self.shortCutPath):
            utils.deleteFile(self.shortCutPath)
        return super().unmerge()

from Package.MaybeVirtualPackageBase import *

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, OsUtils.isWin(), classA=WinPackage)
