    Section "Un.Cleanup Stray Files"
        RMDir /r /rebootok  $INSTDIR\bin
        RMDir /REBOOTOK $INSTDIR
    SectionEnd
    
    Section "Un.Cleanup Regsistry"
        SetRegView 64
        DeleteRegKey SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}"
        DeleteRegKey SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegKey SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegKey SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegValue SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}"
        DeleteRegValue SHCTX "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\" "$INSTDIR\bin\kdiff3.exe"

        SetRegView 32
        ;remove old diff-ext settings
        DeleteRegKey HKCU  "Software\KDiff3"
        ;Maybe left behind due to a bug in previous installers.
        DeleteRegKey SHCTX  "Software\KDE\KDiff3"
        DeleteRegKey /ifempty SHCTX  "Software\KDE\"
    SectionEnd
    