import streamlit as st
from llm_functions import *
from mermaid_functions import *
from utils import *


# ---------------------------
# Streamlit UI
# ---------------------------

st.title("Codiagram LM by Fredator")

input_type = st.radio("Type d'entrée", ["Code", "Texte"])

classes = []
relations = []
placeholder = st.empty()

# Stocker la dernière réponse de l'IA
if "last_mermaid" not in st.session_state:
    st.session_state.last_mermaid = ""


if input_type == "Texte":

    # Affichage de la dernière réponse
    if st.session_state.last_mermaid:
        st.subheader("Dernière réponse Mermaid de l'IA")
        st.text_area(st.session_state.last_mermaid)

    text_input = st.text_area("Entrez le texte :", height=200)
    if st.button("Obtenir des explication"):
       
       if placeholder:
            placeholder.empty()
       placeholder.info("L'IA analyse le texte…")
       with st.spinner("please wait"):
            explanation_text = explanation_with_llm(text_input)
       # Afficher le texte complet (Mermaid + explications)
       st.text_area("Réponse de l'IA", explanation_text, height=300)

       # On met à jour le state pour affichage
       st.session_state.last_mermaid = explanation_text

# elif input_type == "Image":
#     uploaded_file = st.file_uploader("Téléversez une image (PNG/JPG)", type=["png", "jpg", "jpeg"])
#     if uploaded_file and st.button("Générer Diagramme"):
#         with open("temp_image.png", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         classes = ocr_image("temp_image.png")
#         relations = st.text_area("Relations (optionnel, ex: A --> B)").splitlines()
#         code = generate_mermaid(classes, relations, diagram_type)
#         st.code(code, language="mermaid")
#         png_file = export_mermaid(code, f"diagram_{diagram_type}.png")
#         st.image(png_file, caption="Diagramme généré")

# if input_type == "Fichier Visio":
#     uploaded_file = st.file_uploader("Téléversez un fichier Visio (.vsdx)", type=["vsdx"])
#     if uploaded_file and st.button("Générer Diagramme"):
#         with open("temp.vsdx", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         classes, relations = parse_visio("temp.vsdx")
#         code = generate_mermaid(classes, relations, diagram_type)
#         st.code(code, language="mermaid")
#         png_file = export_mermaid(code, f"diagram_{diagram_type}.png")
#         st.image(png_file, caption="Diagramme généré")

elif input_type == "Code":
    code_cs = st.text_area("Collez votre code ici", height=200)

    # Affichage de la dernière réponse
    if st.session_state.last_mermaid:
        st.subheader("Dernière réponse Mermaid de l'IA")
        st.code(st.session_state.last_mermaid, language="mermaid")

    if st.button("Obtenir explications"):
        with st.spinner("Please wait"):
            st.subheader("Explications et analyse")

            placeholder.empty()
            placeholder.info("L'IA analyse le code…")

            raw_mermaid = analyze_with_llm(code_cs)

            # Afficher le texte complet (Mermaid + explications)
            st.text_area("Réponse de l'IA", raw_mermaid, height=300)

    if st.button("Générer le diagramme"):

        diagram_type = st.selectbox("Choisir le type de diagramme",("class", "usecase", "sequence", "activity"))
        placeholder = st.empty()
        placeholder.info("L'IA analyse le code…")

        mermaid_code = ""
        png_file = None

        with st.spinner("Please wait"):

            try:
                raw_mermaid = generate_diagram_with_llm(code_cs, diagram_type)
                mermaid_code = clean_mermaid_only(raw_mermaid)

                # On met à jour le state pour affichage
                st.session_state.last_mermaid = mermaid_code

                st.subheader("Diagramme Mermaid")
                st.code(raw_mermaid, language="mermaid")

                # Génération image PNG
                png_file = export_mermaid(mermaid_code, "diagram_csharp.svg")
                # st.image(png_file, caption="Diagramme généré")

            except Exception as e:
                st.error(f"Erreur lors de la génération du diagramme : {e}")

        # Affichage final

        st.success("Génération réussi")
        if mermaid_code:
            st.subheader("Code Mermaid")
            st.code(mermaid_code, language="mermaid")
        if png_file:
            st.subheader("Diagramme généré")
            st.image("diagram_csharp.svg")
