import xml.etree.ElementTree as ET

en_strings = {'stat_activity': '%1$s Activity'}
ar_strings = {'stat_activity': 'نشاط %1$s'}

def add_strings(file_path, strings_dict):
    tree = ET.parse(file_path)
    root = tree.getroot()
    existing = {child.attrib['name'] for child in root if 'name' in child.attrib}
    for key, val in strings_dict.items():
        if key not in existing:
            elem = ET.SubElement(root, 'string', {'name': key})
            elem.text = val
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

add_strings('app/src/main/res/values/strings.xml', en_strings)
add_strings('app/src/main/res/values-ar/strings.xml', ar_strings)

file_path = "app/src/main/java/com/example/ui/screens/profile/PublicProfileScreen.kt"
with open(file_path, "r") as f:
    content = f.read()
content = content.replace('Text("$selectedStat Activity",', 'Text(stringResource(R.string.stat_activity, selectedStat),')
with open(file_path, "w") as f:
    f.write(content)

