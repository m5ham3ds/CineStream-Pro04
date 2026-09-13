def add_to_xml(filepath, is_ar=False):
    with open(filepath, 'r') as f:
        content = f.read()

    to_add = []
    
    if is_ar:
        if 'name="confirm_change"' not in content: to_add.append('    <string name="confirm_change">تأكيد التغيير</string>')
        if 'name="confirm_theme_change"' not in content: to_add.append('    <string name="confirm_theme_change">هل أنت متأكد من تغيير المظهر؟</string>')
        if 'name="confirm_color_change"' not in content: to_add.append('    <string name="confirm_color_change">هل أنت متأكد من تغيير اللون الأساسي؟</string>')
        if 'name="confirm_language_change"' not in content: to_add.append('    <string name="confirm_language_change">هل أنت متأكد من تغيير اللغة؟ سيتم إعادة التشغيل.</string>')
        if 'name="yes"' not in content: to_add.append('    <string name="yes">نعم</string>')
    else:
        if 'name="confirm_change"' not in content: to_add.append('    <string name="confirm_change">Confirm Change</string>')
        if 'name="confirm_theme_change"' not in content: to_add.append('    <string name="confirm_theme_change">Are you sure you want to change the theme?</string>')
        if 'name="confirm_color_change"' not in content: to_add.append('    <string name="confirm_color_change">Are you sure you want to change the primary color?</string>')
        if 'name="confirm_language_change"' not in content: to_add.append('    <string name="confirm_language_change">Are you sure you want to change the language? This requires a restart.</string>')
        if 'name="yes"' not in content: to_add.append('    <string name="yes">Yes</string>')

    if to_add:
        content = content.replace('</resources>', '\n'.join(to_add) + '\n</resources>')
        with open(filepath, 'w') as f:
            f.write(content)

add_to_xml('app/src/main/res/values/strings.xml', False)
add_to_xml('app/src/main/res/values-ar/strings.xml', True)
