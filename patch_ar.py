with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content = f.read()

content = content.replace("</resources>", '    <string name="help_support">المساعدة والدعم</string>\n    <string name="confirm_sign_out">هل أنت متأكد أنك تريد تسجيل الخروج؟</string>\n</resources>')

with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(content)
