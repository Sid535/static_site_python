import os, shutil, sys
from generate_page import generate_pages_recursive


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  


def copy_static_to_public(static_dir: str, docs_dir: str) -> None:
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            file_path = os.path.join(docs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.makedirs(docs_dir)
        
    copy_recursive(static_dir, docs_dir)
    
def copy_recursive(static_dir: str, docs_dir: str) -> None:
    for item in os.listdir(static_dir):
        static_path = os.path.join(static_dir, item)
        docs_path = os.path.join(docs_dir, item)
        
        if os.path.isfile(static_path):
            shutil.copy(static_path, docs_path) 
        elif os.path.isdir(static_path):
            os.makedirs(docs_path, exist_ok=True)
            copy_recursive(static_path, docs_path)
            

def main() -> None:
    static_dir = os.path.join(project_root, "static")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    docs_dir = os.path.join(project_root, "docs")
    
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_static_to_public(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    
    
if __name__ == '__main__':
    main()