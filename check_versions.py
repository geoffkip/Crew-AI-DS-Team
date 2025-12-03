import json
import urllib.request
import sys

packages = [
    "pandas",
    "python-pptx",
    "crewai",
    "langchain-google-genai",
    "langchain",
    "scikit-learn",
    "litellm"
]

print("Fetching latest versions...")
for pkg in packages:
    try:
        url = f"https://pypi.org/pypi/{pkg}/json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
            print(f"{pkg}=={data['info']['version']}")
    except Exception as e:
        print(f"# Error fetching {pkg}: {e}")
