import os
import re

old_button_html = """<!-- Back Button -->
<button onclick="history.back()" style="position: fixed; top: 20px; left: 20px; width: 40px; height: 40px; border-radius: 50%; background-color: white; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; z-index: 9999; display: flex; align-items: center; justify-content: center; color: black;" title="Go Back">
    <i class="fas fa-arrow-left"></i>
</button>"""

new_button_html = """<!-- Back Button -->
<button onclick="history.back()" style="position: fixed; top: 20px; left: 20px; width: 40px; height: 40px; border-radius: 50%; background-color: white; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; z-index: 9999; display: flex; align-items: center; justify-content: center; color: black; font-size: 20px; font-weight: bold;" title="Go Back">
    &#8592;
</button>"""

templates_dir = "templates"

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remove the old block completely and optionally remove any leading/trailing newlines
            if old_button_html in content:
                content = content.replace(old_button_html, new_button_html)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {path}")
            elif "history.back()" not in content and "<body>" in content:
                content = content.replace("<body>", f"<body>\n{new_button_html}")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Newly added {path}")
