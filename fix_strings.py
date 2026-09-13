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
    'category_movies': 'Movies',
    'category_series': 'Series',
    'category_anime': 'Anime',
    'category_genres': 'Genres',
    'category_top_rated': 'Top Rated',
    'trending_movies': 'Trending Movies',
    'trending_series': 'Trending Series',
    'trending_anime': 'Trending Anime'
}

ar_strings = {
    'category_movies': 'الأفلام',
    'category_series': 'المسلسلات',
    'category_anime': 'الأنمي',
    'category_genres': 'التصنيفات',
    'category_top_rated': 'الأعلى تقييماً',
    'trending_movies': 'أفلام رائجة',
    'trending_series': 'مسلسلات رائجة',
    'trending_anime': 'أنمي رائج'
}

add_strings('app/src/main/res/values/strings.xml', en_strings)
add_strings('app/src/main/res/values-ar/strings.xml', ar_strings)
