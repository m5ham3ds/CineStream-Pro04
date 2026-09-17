import re

def add_string_res(file_path, name, value):
    with open(file_path, "r") as f:
        content = f.read()
    if f'<string name="{name}">' not in content:
        content = content.replace("</resources>", f'    <string name="{name}">{value}</string>\n</resources>')
        with open(file_path, "w") as f:
            f.write(content)

add_string_res("app/src/main/res/values/strings.xml", "not_released_yet", "This work has not been released yet, but will be available soon.")
add_string_res("app/src/main/res/values/strings.xml", "ok_button", "OK")

add_string_res("app/src/main/res/values-ar/strings.xml", "not_released_yet", "هذا العمل لم يُعرض بعد، ولكنه سيعرض قريباً.")
add_string_res("app/src/main/res/values-ar/strings.xml", "ok_button", "حسناً")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace('Text("هذا العمل لم يُعرض بعد، ولكنه سيعرض قريباً."', 'Text(stringResource(R.string.not_released_yet)')
content = content.replace('Text("حسناً"', 'Text(stringResource(R.string.ok_button)')

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

