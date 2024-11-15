import ollama
import requests

# load a list of all agents from AIOS

json = requests.get('https://openagi-beta.vercel.app/api/get_all_agents').json()

for agent in json:
    if agent['name'] == "academic_agent":
        agent['description'] = "Find academic papers related to a given topic on ArXiv."

# construct the system prompt
prompt = "\n".join([agent['name'] + ": " + agent['description'] for agent in json])

response = ollama.chat(model='llama3', messages=[
  {
    'role': 'system',
    'content': prompt
  },
  {
    'role': 'user',
    'content': 'What is the topic of my paper?'
  }
])
print(response['message']['content'])


