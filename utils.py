import re
import zipfile
import xml.etree.ElementTree as ET
import cv2
import pytesseract
import unidecode


def ocr_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    classes = [line.strip() for line in text.splitlines() if line.strip()]
    return classes

def parse_visio(vsdx_path):
    classes = {}
    relations = []

    with zipfile.ZipFile(vsdx_path, 'r') as zf:
        for name in zf.namelist():
            if "visio/pages/page" in name and name.endswith(".xml"):
                xml_content = zf.read(name)
                root = ET.fromstring(xml_content)

                # 1️⃣ récupérer toutes les formes avec leur ID
                for shape in root.iter('{http://schemas.microsoft.com/office/visio/2012/main}Shape'):
                    shape_id = shape.attrib.get('ID')
                    txt = ''.join(shape.itertext()).strip()
                    if txt and shape_id:
                        classes[shape_id] = sanitize_name(txt)

                # 2️⃣ récupérer toutes les connexions
                for connector in root.iter('{http://schemas.microsoft.com/office/visio/2012/main}Connect'):
                    from_id = connector.attrib.get('FromSheet')
                    to_id = connector.attrib.get('ToSheet')
                    if from_id in classes and to_id in classes:
                        relations.append(f"{classes[from_id]} --> {classes[to_id]}")

    return list(classes.values()), relations

# def parse_csharp_code(code_cs):
#     """Parse simplifié C# pour extraire classes et relations"""
#     classes = []
#     relations = []
#     # Classes
#     class_matches = re.findall(r'class\s+(\w+)(?:\s*:\s*(\w+))?', code_cs)
#     for match in class_matches:
#         class_name = match[0]
#         parent = match[1]
#         classes.append(class_name)
#         if parent:
#             relations.append(f"{class_name} --> {parent}")
#     # Propriétés et méthodes simplifiées
#     props = re.findall(r'(public|private|protected)\s+([\w<>]+)\s+(\w+)\s*\{', code_cs)
#     for p in props:
#         cls = class_matches[0][0] if class_matches else "Unknown"
#         classes.append(f"{cls} : +{p[2]} : {p[1]}")
#     return list(set(classes)), relations

def sanitize_name(name):
    """
    Transforme n'importe quel texte en identifiant Mermaid valide :
    - Supprime accents
    - Remplace tout ce qui n'est pas lettre/chiffre par _
    - Supprime underscores en début/fin
    - Remplace retours chariot / saut de ligne par _
    """
    if not name:
        return "Unknown"
    name = unidecode.unidecode(name)           # accents
    name = name.replace('\n', '_').replace('\r', '_')  # sauts de ligne
    name = re.sub(r'[^0-9a-zA-Z]+', '_', name)  # tout sauf lettres/chiffres -> _
    name = re.sub(r'_+', '_', name)            # plusieurs _ -> 1 seul
    name = name.strip('_')
    if not name:
        return "Unknown"
    return name
