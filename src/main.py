import os, shutil
from generate_page import generate_pages_recursive


def copy_static_to_public() -> None:
    src_dir = '/home/siddesh/myprojects/Github/static_site_python/static'
    dst_dir = '/home/siddesh/myprojects/Github/static_site_python/public'
    if os.path.exists(dst_dir):
        for filename in os.listdir(dst_dir):
            file_path = os.path.join(dst_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.makedirs(dst_dir)
        
    copy_recursive(src_dir, dst_dir)
    
def copy_recursive(src_dir: str, dst_dir: str) -> None:
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path) 
        elif os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            copy_recursive(src_path, dst_path)
            

def main() -> None:
    copy_static_to_public()
    
    src_dir = '/home/siddesh/myprojects/Github/static_site_python/content/'
    template_path = '/home/siddesh/myprojects/Github/static_site_python/template.html'
    dst_dir = '/home/siddesh/myprojects/Github/static_site_python/public/'
    
    generate_pages_recursive(src_dir, template_path, dst_dir)
    
    
if __name__ == '__main__':
    main()