import os
import json


def files_info(base_dir: str) -> dict:
    file_list = {}
    for (root, _dirs, files) in  os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            file_list[full_path.replace(base_dir, '')] = {
                "full_path": full_path,
                "size" : os.path.getsize(os.path.join(root, file))
            }
    return file_list

def json_to_file(value: dict, file: str):
    with open(file, 'w') as fp:
        json.dump(value, fp)

if __name__ == '__main__':
    base_dir = "C:\\Users\\tlab\\photo"
    base_info = files_info(base_dir)

    cmp_dir  = "F:\\tk_backup\\개인문서"
    cmp_info = files_info(cmp_dir)

    base_exist = {}
    base_diff = {}
    base_not_exist = {}
    cmp_not_exist = {}

    for k,v in base_info.items():
        citem = cmp_info.pop(k, None)
        if citem:
            if citem.get('size') == v.get('size'):
                base_exist[k] = v
            else:
                base_diff[k] = v
        else:
            cmp_not_exist[k] = v

    base_not_exist = cmp_info
    print(base_diff)
    print(base_not_exist)
    