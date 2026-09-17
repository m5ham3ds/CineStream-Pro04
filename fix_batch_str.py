with open("app/src/main/res/values/strings.xml", "r") as f:
    content = f.read()
if '<string name="batch_download">' not in content:
    content = content.replace("</resources>", '    <string name="batch_download">Batch Download</string>\n</resources>')
    with open("app/src/main/res/values/strings.xml", "w") as f:
        f.write(content)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content_ar = f.read()
if '<string name="batch_download">' not in content_ar:
    content_ar = content_ar.replace("</resources>", '    <string name="batch_download">التحميل الجماعي</string>\n</resources>')
    with open("app/src/main/res/values-ar/strings.xml", "w") as f:
        f.write(content_ar)

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    c = f.read()
if "import com.example.R" not in c:
    c = c.replace("package com.example.ui.components", "package com.example.ui.components\n\nimport com.example.R\nimport androidx.compose.ui.res.stringResource")
    with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
        f.write(c)

