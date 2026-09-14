import xml.etree.ElementTree as ET

def add_strings(file_path, strings_dict):
    try:
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
    except Exception as e:
        print(f"Error on {file_path}: {e}")

en_strings = {
    'top_movies': 'Top Movies',
    'top_shows': 'Top TV Shows'
}

ar_strings = {
    'top_movies': 'أفضل الأفلام',
    'top_shows': 'أفضل المسلسلات'
}

add_strings('app/src/main/res/values/strings.xml', en_strings)
add_strings('app/src/main/res/values-ar/strings.xml', ar_strings)
