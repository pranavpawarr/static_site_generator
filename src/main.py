import os
import shutil
from textnode import TextNode,InlineTextType
from markdown_to_blocks import markdown_to_html_node, extract_title

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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()
    
    # markdown_to_html_node returns a ParentNode object
    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)

    # Convert the ParentNode to an HTML string
    html_content = html_node.to_html()

    # Replace placeholders in template
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Create parent directories if needed
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(final_html)
    
    print(f"Page generated successfully at {dest_path}")

def main():
    # Copy static files to public directory
    copy_static_to_public()
    
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

    # Your existing test code
    node = TextNode("This is some anchor text", InlineTextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()