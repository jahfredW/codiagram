# Codiagram

  

## 1 - installation des pré-requis

  

-   **Télecharger et** **Installer Python 3.10+** [https://www.python.org/downloads/](https://www.python.org/downloads/)
-   **Installer Java** (nécessaire pour PlantUML) [https://www.java.com/fr/download/manual.jsp](https://www.java.com/fr/download/manual.jsp)
-   **Installer Node.js** (pour Mermaid CLI) [https://nodejs.org/en/download/current](https://nodejs.org/en/download/current)
-   **Installer Tesseract OCR** [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
-   **Installer les bibliothèques Python** suivante avec pip

pip install opencv-python pytesseract vsdx python-mermaid

pip install pillow chat

  

## 2 - Mise à jour de la politique de sécurité d'exécution des scripts

  

-   Ouvrir PowerShell en mode admin
-   éxécuter la commande suivante pour une mise à jour permanente :

```PowerShell
Set-ExecutionPolicy RemoteSigned
```

- Ou mise à jour temporaire pour la session en cours
```PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## 3 - Tester le fonctionnement de NPM (Node Packet Manager)
```PowerShell
npm -v
```
Si lle numéro de version apparait, l'intallation est ok 

## 4 - Installer Mermail CLi
```PowerShell
npm install -g @mermaid-js/mermaid-cli
```

## 5 - Installer StreamLit
En ligne de commande via un terminal ou PowerShell
```PowerShell
python -m pip install streamlit
```

Puis vérifier si il est bien installé
```PowerShell
python -m pip show streamlit
```

## 6 - Mise à jour des variables d'environnement si nécessaire
Voici la commande qui permet de vérifier la liste des path : 
```PowerShell
echo $env:PATH
```

## 7 - Exécuter l'application
Exécuter main.py avc streamlit via la commande : 
```PowerShell
streamlit run main.py
```

Ou sans dépendre des vairables d'environnement : 
```PowerShell
python -m streamlit run main.py
```


> Enjoy :) ;) 
