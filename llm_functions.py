from ollama import chat

# ---------------------------
# Fonctions principales
# ---------------------------

def generate_diagram_with_llm(code, diagram_type):

    prompt = f"""
You are a software architect.

return:
- Mermaid diagram langage script witch type is {diagram_type} ONLY
- If it's not possible to make a {diagram_type} diagram, make a diagram which could easily help the developper to understand 
- This could be It can be any type of diagram
- Just Mermaid script in the response ! Nothing else ! In order To generate digram after

Code:
{code}
"""
    response = chat(
        model='deepseek-coder', 
        stream=False, 
        messages=[{'role': 'user', 'content': prompt}])
    #print(response.message.content)
    # response = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={
    #         "model": "llama2-13b",
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )

    data = response.message.content
    #data = response.json()
    # Récupération du texte généré
    return data



def analyze_with_llm(code):

    prompt = f"""
You are a software architect.

Analyze this code and return:
- list of classes if exists
- relations if exits
- detailled explanation
- What the code is suppose to do
- Anything which could help developper

Please make the response in French Langage
Code:
{code}
"""

    response = chat(
        model='deepseek-coder', 
        stream=False, 
        messages=[{'role': 'user', 'content': prompt}])
    # response = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={
    #         "model": "llama2-13b",
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )

    data = response.message.content
    #data = response.json()
    # Récupération du texte généré
    return data


def explanation_with_llm(text):

    prompt = f"""

Analyze and explain the following text. 
Provide a clear and structured explanation.

Please make the response in French Langage
Text:
{text}
"""

    response = chat(
        model='deepseek-coder', 
        stream=False, 
        messages=[{'role': 'user', 'content': prompt}])

    data = response.message.content
    return data