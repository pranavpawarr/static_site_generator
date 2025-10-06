import os
import shutil
from textnode import TextNode,InlineTextType

def copy_static_to_public(source="static",destination="public"):
    if os.path.exists(destination):
        print(f"Deleting existing directory: {destination}")
        shutil.rmtree(destination)
    
    print(f"Creating directory: {destination}")
    os.mkdir(destination)

    copy_directory_recursive(source, destination)
    print(f"\nCopy complete: {source} -> {destination}")

def copy_directory_recursive(source, destination):
    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source,item)
        dest_path = os.path.join(destination,item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copying file: {source_path} -> {dest_path}")
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_recursive(source_path, dest_path)


    
def main():
    # Copy static files to public directory
    copy_static_to_public()
    
    # Your existing test code
    node = TextNode("This is some anchor text", InlineTextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()