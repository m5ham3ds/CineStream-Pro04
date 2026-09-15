def add_strings(filepath, strings):
    with open(filepath, "r") as f:
        c = f.read()
    c = c.replace("</resources>", strings + "\n</resources>")
    with open(filepath, "w") as f:
        f.write(c)

en_strings = """
    <string name="delete_download_title">Delete %1$s</string>
    <string name="delete_download_desc">Are you sure you want to permanently delete this download? This action cannot be undone.</string>
    <string name="delete_confirm">Delete</string>
    <string name="cancel">Cancel</string>
"""
add_strings("app/src/main/res/values/strings.xml", en_strings)

ar_strings = """
    <string name="delete_download_title">حذف %1$s</string>
    <string name="delete_download_desc">هل أنت متأكد أنك تريد حذف هذا التنزيل نهائياً؟ لا يمكن التراجع عن هذا الإجراء.</string>
    <string name="delete_confirm">حذف</string>
    <string name="cancel">إلغاء</string>
"""
add_strings("app/src/main/res/values-ar/strings.xml", ar_strings)
