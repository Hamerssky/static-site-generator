import os
import shutil
from markdown_to_html_node import markdown_to_html_node

def clone_static_public():
    shutil.rmtree(f"./public")
    print(f"Deleting public")
    os.makedirs("./public/")
    print("Creating public directory")

    clone_to_path("./static", "./public")

    print("Successfully cloned")

def clone_to_path(source_path, dest_path):
    if not os.path.exists(source_path):
        raise ValueError("Invalid source path")
    
    for path in os.listdir(source_path):
        source = f"{source_path}/{path}"
        dest = f"{dest_path}/{path}"
        print(f"Cloning {source} to {dest}")
        if os.path.isfile(source):
            shutil.copy(source, dest)
            continue
        os.makedirs(dest)
        clone_to_path(source, dest)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(dest_path, exist_ok = True)
    with open(f"{dest_path}/index.html", "w") as file:
        file.write(page)

    print("Successfully generated the page")

def main():
    print("Executing main function")
    clone_static_public()
    generate_page("./content/index.md", "./template.html", "./public")

if __name__ == "__main__":
    main()