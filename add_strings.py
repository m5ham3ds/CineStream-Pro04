import xml.etree.ElementTree as ET

def add_strings(file_path, strings_dict):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    existing = {child.attrib['name'] for child in root if 'name' in child.attrib}
    
    for key, val in strings_dict.items():
        if key not in existing:
            elem = ET.SubElement(root, 'string', {'name': key})
            elem.text = val
            
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

en_strings = {
    'connecting_to': 'Connecting to %1$s...',
    'loading_site': 'Loading %1$s...',
    'current_site': 'Current Site: %1$s',
    'used_space': '%1$s / %2$s used',
    'used_percentage': '%1$d%% used',
    'free_space': '%1$s free',
    'episodes_count': '%1$d Episodes',
    'connected_to': 'Connected to %1$s',
    'sent': 'Sent',
    'received': 'Received',
    'completed': 'Completed'
}

ar_strings = {
    'connecting_to': 'جاري الاتصال بـ %1$s...',
    'loading_site': 'جاري تحميل %1$s...',
    'current_site': 'الموقع الحالي: %1$s',
    'used_space': 'مُستخدم %1$s / %2$s',
    'used_percentage': 'مُستخدم %1$d%%',
    'free_space': '%1$s مساحة حرة',
    'episodes_count': '%1$d حلقات',
    'connected_to': 'متصل بـ %1$s',
    'sent': 'تم الإرسال',
    'received': 'تم الاستلام',
    'completed': 'مكتمل'
}

add_strings('app/src/main/res/values/strings.xml', en_strings)
add_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

