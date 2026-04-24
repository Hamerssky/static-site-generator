import os
import shutil
from markdown_to_html_node import markdown_to_html_node
import argparse

def clone_static(basepath, folder_name):
    path = os.path.join(basepath, folder_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleting {folder_name}")
    os.makedirs(path)
    print(f"Creating {folder_name} directory")

    clone_to_path(os.path.join(basepath, "static"), os.path.join(basepath, folder_name))

    print("Successfully cloned")

def clone_to_path(source_path, dest_path):
    if not os.path.exists(source_path):
        raise ValueError("Invalid source path")
    
    for path in os.listdir(source_path):
        source = os.path.join(source_path, path)
        dest = os.path.join(dest_path, path)
        print(f"Cloning {source} to {dest}")
        if os.path.isfile(source):
            shutil.copy(source, dest)
        else:
            os.makedirs(dest)
            clone_to_path(source, dest)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    os.makedirs(dest_path, exist_ok = True)
    with open(os.path.join(dest_path, "index.html"), "w") as file:
        file.write(page)

    print("Successfully generated the page")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isdir(src_path):
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
        else:
            generate_page(src_path, template_path, dest_dir_path, basepath)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("basepath", nargs = "?", default = "/")
    args = parser.parse_args()
    basepath = args.basepath

    print("Executing main function")

    clone_to = "docs"

    clone_static(basepath, clone_to)

    content_path = os.path.join(basepath, "content")
    template_file = os.path.join(basepath, "template.html")
    cloned_path = os.path.join(basepath, clone_to)
    
    generate_pages_recursive(content_path, template_file, cloned_path, basepath)

    print("Done")

if __name__ == "__main__":
    main()