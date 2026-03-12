import subprocess
import re
import platform
from utils import *




def generate_mermaid(classes, relations, diagram_type="class"):
    code = ""
    classes_clean = [sanitize_name(cl) for cl in classes]

    if diagram_type == "class":
        code = "classDiagram\n"
        for c in classes_clean:
            code += f"    {c}\n"
        for r in relations:
            cleaned = " --> ".join([sanitize_name(x.strip()) for x in r.split("-->")])
            code += f"    {cleaned}\n"

    elif diagram_type == "usecase":
        code = "graph TD\n"
        for c in classes_clean:
            code += f"    {c}\n"
        for r in relations:
            cleaned = " --> ".join([sanitize_name(x.strip()) for x in r.split("-->")])
            code += f"    {cleaned}\n"

    elif diagram_type == "sequence":
        code = "sequenceDiagram\n"
        for r in relations:
            parts = [sanitize_name(x.strip()) for x in r.split("-->")]
            if len(parts) == 2:
                code += f"    {parts[0]}->>{parts[1]}: interaction\n"

    elif diagram_type == "activity":
        code = "flowchart TD\n"
        for c in classes_clean:
            code += f"    {c}\n"
        for r in relations:
            cleaned = " --> ".join([sanitize_name(x.strip()) for x in r.split("-->")])
            code += f"    {cleaned}\n"

    else:
        raise ValueError(f"Type de diagramme inconnu : {diagram_type}")

    return code


def export_mermaid(code, output_file="diagram.png"):
    with open("diagram.mmd", "w") as f:
        f.write(code)

    if platform.system() == "Windows":
        # Sur Windows, il faut utiliser shell=True pour lancer les .cmd
        command = r"npx mmdc -i diagram.mmd -o " + output_file
        subprocess.run(command, shell=True, check=True)
    else:
        # Linux / macOS
        subprocess.run(["npx", "mmdc", "-i", "diagram.mmd", "-o", output_file], check=True)

    return output_file

def clean_mermaid_only(text):
    """
    Extrait uniquement le bloc Mermaid valide et s'arrête avant le texte explicatif.
    """
    # Supprime ```mermaid et ```
    text = text.replace("```mermaid", "").replace("```", "").strip()

    lines = text.splitlines()
    mermaid_started = False
    mermaid_lines = []

    for line in lines:
        stripped = line.strip()
        if not mermaid_started:
            # On détecte le début du diagramme
            if stripped.startswith(("classDiagram", "sequenceDiagram", "flowchart TD")):
                mermaid_started = True
                mermaid_lines.append(stripped)
        else:
            # On ajoute tant que ça ressemble à du code Mermaid
            if stripped == "" or stripped.startswith(("#", "//")):
                continue
            if re.match(r'^(class\s+\w+|[+\-~]\w+|[\w]+ --> [\w]+|{|})', stripped):
                mermaid_lines.append(line)
            else:
                # On stoppe dès que ça ne ressemble plus au code
                break

    if not mermaid_lines:
        raise ValueError("Aucun code Mermaid détecté dans le texte.")

    return "\n".join(mermaid_lines)