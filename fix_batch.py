import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    content = f.read()

content = content.replace('Text("التحميل الجماعي")', 'Text(stringResource(R.string.batch_download))')
content = content.replace('Text("إلغاء")', 'Text(stringResource(R.string.cancel))')

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(content)

