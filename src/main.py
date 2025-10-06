import os
import sys
import shutil
from textnode import TextNode,InlineTextType
from markdown_to_blocks import markdown_to_html_node, extract_title

def copy_static_to_public(source="static", destination="docs"):
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

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"[generate_page] basepath={basepath}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html_content = html_node.to_html()

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    print("[before normalization]", final_html[:300])
    
    # Normalize to root-first (handle both with and without trailing slashes)
    final_html = final_html.replace('href="blog/', 'href="/blog/')
    final_html = final_html.replace('href="contact"', 'href="/contact"')  # No trailing slash
    final_html = final_html.replace('href="contact/', 'href="/contact/')  # With trailing slash
    final_html = final_html.replace('href="index.css"', 'href="/index.css"')
    final_html = final_html.replace('src="images/', 'src="/images/')
    
    print("[after normalization]", final_html[:300])
    
    # Ensure basepath has proper format
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    
    # Diagnostic counts BEFORE basepath replacement
    print("count href-root", final_html.count('href="/'))
    print("count src-root", final_html.count('src="/'))
    
    # Apply basepath replacements (double quotes)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Apply basepath replacements (single quotes)
    final_html = final_html.replace("href='/", f"href='{basepath}")
    final_html = final_html.replace("src='/", f"src='{basepath}")
    
    # Apply basepath replacements (with spaces - less common but possible)
    final_html = final_html.replace('href= "/', f'href="{basepath}')
    final_html = final_html.replace("href= '/", f"href='{basepath}")
    
    # Diagnostic counts AFTER basepath replacement
    print("count href-base", final_html.count(f'href="{basepath}'))
    print("count src-base", final_html.count(f'src="{basepath}'))
    print("[after basepath]", final_html[:300])

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)



# py
def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath="/"):
    os.makedirs(dest_dir_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(item_path, template_path, dest_path, basepath)
        elif os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursively(item_path, template_path, new_dest_dir, basepath)
def main():
    # Default to GitHub Pages basepath if not provided
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/static_site_generator/"  # Your repo name
    
    copy_static_to_public(source="static", destination="docs")
    generate_pages_recursively("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()