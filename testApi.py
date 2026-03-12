from ollama import chat

response = chat(model='llama2:13b', messages=[
    {'role': 'user', 'content': 'Comment ça va ?.'}
])
print(response.message.content)