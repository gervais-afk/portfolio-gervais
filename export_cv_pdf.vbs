' Compatibility launcher: regenerate from profile.json, validate, then publish PDFs/DOCX.
' Never exports an independently edited DOCX over the canonical PDFs.
Option Explicit
Dim shell, fs, folder, python, command, result
Set shell = CreateObject("WScript.Shell")
Set fs = CreateObject("Scripting.FileSystemObject")
folder = fs.GetParentFolderName(WScript.ScriptFullName)
python = shell.ExpandEnvironmentStrings("%USERPROFILE%") & "\anaconda3\python.exe"
If fs.FileExists(python) Then
    command = Chr(34) & python & Chr(34)
Else
    command = "py -3"
End If
command = command & " -B -X utf8 " & Chr(34) & folder & "\build_cv.py" & Chr(34)
result = shell.Run(command, 1, True)
If result = 0 Then
    MsgBox "CV FR/EN regenerated and validated: one A4 page per PDF. DOCX files updated from profile.json.", 64, "CV export"
Else
    MsgBox "CV generation failed. See the Python output. Existing published assets are preserved if validation fails.", 16, "CV export"
End If
WScript.Quit result
