' ============================================================
' export_cv_pdf.vbs
' Double-click this file to export both CV DOCX files to PDF
' ============================================================

Dim oWord, oDoc
Dim sFolder

sFolder = "c:\Users\HP\Desktop\portfolio-gervais\"

Dim files(1)
files(0) = sFolder & "KOA_MARIE_GERVAIS_NELLY_CV_FR.docx"
files(1) = sFolder & "KOA_MARIE_GERVAIS_NELLY_CV_EN.docx"

Dim pdfs(1)
pdfs(0) = sFolder & "KOA_MARIE_GERVAIS_NELLY_CV FR.pdf"
pdfs(1) = sFolder & "KOA_MARIE_GERVAIS_NELLY_CV_EN.pdf"

Set oWord = CreateObject("Word.Application")
oWord.Visible = False
oWord.DisplayAlerts = 0

Dim i
For i = 0 To 1
    If CreateObject("Scripting.FileSystemObject").FileExists(files(i)) Then
        Set oDoc = oWord.Documents.Open(files(i), False, True) ' ReadOnly
        oDoc.ExportAsFixedFormat pdfs(i), 17, False, 0  ' 17 = wdExportFormatPDF
        oDoc.Close False
        MsgBox "Exported: " & pdfs(i), 64, "CV Export"
    Else
        MsgBox "File not found: " & files(i), 48, "CV Export"
    End If
Next

oWord.Quit
MsgBox "Both CVs exported to PDF successfully!", 64, "CV Export Done"
