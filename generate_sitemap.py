import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

def parse_toml_items(text):
    """Simple extraction of paths from TOML items/nested items."""
    paths = []
    # Match notebook paths
    paths.extend(re.findall(r'path\s*=\s*"([^"]+\.ipynb)"', text))
    # Match image paths
    paths.extend(re.findall(r'path\s*=\s*"([^"]+\.jpg)"', text))
    # Match extra_img paths
    paths.extend(re.findall(r'extra_img\s*=\s*"([^"]+)"', text))
    # Match subsection image paths
    paths.extend(re.findall(r'image\s*=\s*"([^"]+)"', text))
    return sorted(list(set(paths)))

def generate_sitemap():
    base_url = "https://statistics.kavakci.dev/"
    
    try:
        with open("notes.toml", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("notes.toml not found.")
        return

    paths = parse_toml_items(content)
    
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Root URL
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = base_url
    ET.SubElement(url, "priority").text = "1.0"

    for p in paths:
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        if p.endswith(".ipynb"):
            loc.text = f"{base_url}notebook.html?nb={p}"
        else:
            loc.text = f"{base_url}viewer.html?img={p}"

    # Pretty print XML
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    # Remove extra empty lines from minidom
    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])

    with open("sitemap.xml", "w") as f:
        f.write(pretty_xml)
    
    print(f"Generated sitemap.xml with {len(paths) + 1} URLs.")

if __name__ == "__main__":
    generate_sitemap()
