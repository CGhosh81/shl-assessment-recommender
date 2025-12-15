import requests

url = "http://127.0.0.1:8000/recommend"

payload = {
    "query": "I am hiring Java developers who can collaborate with business teams. The test should be around 40 minutes.",
    "top_k": 5
}

response = requests.post(url, json=payload)

results = response.json()

for i, r in enumerate(results, 1):
    print(f"\nResult {i}")
    print("Name:", r["name"])
    print("Duration:", r["duration_minutes"])
    print("Test Type:", r["test_type"])
    print("URL:", r["url"])
