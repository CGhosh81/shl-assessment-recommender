import os

structure = {
  
        "shl_recommender.py": "",
        "requirements.txt": "",
        "README.md": "",
        "data": {
            "Gen_AI_Dataset.xlsx": "",
            "product_catalog.json": ""
        },
        "notebooks": {
  
        },
        "web": {
            "index.html": "",
            "style.css": ""
        }
    }


def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            open(path, "w", encoding="utf-8").close()

create_structure(".", structure)
print("Project structure created successfully.")
