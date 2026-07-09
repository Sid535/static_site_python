import os
from blocknode import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped == "#":
            return ""
    raise ValueError("No h1 header found in markdown")
    
def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str | None = "/") -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        src_content = f.read()
    
    with open(template_path) as f:
        template_content = f.read()
    
    html_content = markdown_to_html_node(src_content).to_html()
    html_title = extract_title(src_content)
    
    template_content = template_content.replace(r"{{ Title }}", html_title, 1)
    template_content = template_content.replace(r"{{ Content }}", html_content, 1)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_path):
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str | None = "/") -> None:
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dst_path = dst_path[:-2]
                dst_path += "html"
                generate_page(src_path, template_path, dst_path, basepath)
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dst_path, basepath)