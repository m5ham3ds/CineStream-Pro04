import xml.etree.ElementTree as ET

def add_strings(file_path, strings_dict):
    tree = ET.parse(file_path)
    root = tree.getroot()
    existing = {child.attrib['name'] for child in root if 'name' in child.attrib}
    
    for key, val in strings_dict.items():
        if key not in existing:
            elem = ET.SubElement(root, 'string', {'name': key})
            elem.text = val
        else:
            for child in root:
                if child.attrib.get('name') == key:
                    child.text = val
                    
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

en_strings = {
    'premium_user': 'Premium User',
    'free_account': 'Free Account',
    'guest_user': 'Guest User',
    'log_out': 'Log Out',
    'library': 'Library'
}

ar_strings = {
    'premium_user': 'مستخدم مميز',
    'free_account': 'حساب مجاني',
    'guest_user': 'مستخدم زائر',
    'log_out': 'تسجيل الخروج',
    'library': 'المكتبة'
}

add_strings('app/src/main/res/values/strings.xml', en_strings)
add_strings('app/src/main/res/values-ar/strings.xml', ar_strings)
