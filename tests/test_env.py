import requests

url = "https://huggingface.co/spaces/practiceof/eadi-openenv/reset"
resp = requests.post(url)
print(resp.status_code, resp.json())