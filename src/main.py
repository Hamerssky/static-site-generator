import os
import shutil

def clone_static_public():
    shutil.rmtree(f"./public")
    print(f"Deleting public")
    os.makedirs("./public/")
    print("Creating public directory")

    clone_to_path("./static", "./public")

    print("Succesfully cloned")

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

def main():
    print("Executing main function")
    clone_static_public()

if __name__ == "__main__":
    main()