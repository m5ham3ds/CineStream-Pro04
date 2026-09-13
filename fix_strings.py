def add_to_xml(filepath, is_ar=False):
    with open(filepath, 'r') as f:
        content = f.read()

    to_add = []
    
    if is_ar:
        if 'name="cancel"' not in content: to_add.append('    <string name="cancel">إلغاء</string>')
        if 'name="movies"' not in content: to_add.append('    <string name="movies">الأفلام</string>')
        if 'name="about_app"' not in content: to_add.append('    <string name="about_app">حول التطبيق</string>')
    else:
        if 'name="cancel"' not in content: to_add.append('    <string name="cancel">Cancel</string>')
        if 'name="movies"' not in content: to_add.append('    <string name="movies">Movies</string>')
        if 'name="about_app"' not in content: to_add.append('    <string name="about_app">About CineStream</string>')

    if to_add:
        content = content.replace('</resources>', '\n'.join(to_add) + '\n</resources>')
        with open(filepath, 'w') as f:
            f.write(content)

add_to_xml('app/src/main/res/values/strings.xml', False)
add_to_xml('app/src/main/res/values-ar/strings.xml', True)
