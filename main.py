import os
import re
from pathlib import Path


def find_dll_files(root_dir):
    """查找根目录下所有的DLL文件，排除modengine2目录"""
    dll_files = []
    print("找到的DLL文件:")
    for root, dirs, files in os.walk(root_dir):
        # 排除modengine2目录
        if 'modengine2' in root:
            continue
        for file in files:
            if file.lower().endswith('.dll'):
                dll_path = os.path.join(root, file)
                # 获取相对路径
                rel_path = os.path.relpath(dll_path, root_dir)
                # 转换路径分隔符为双反斜杠
                dll_files.append(rel_path.replace('\', '\\'))
                print(f"  {dll_path}")
    print(f"共找到 {len(dll_files)} 个DLL文件")
    return dll_files


def is_mod_folder(folder_path):
    """判断文件夹是否为MOD文件夹"""
    mod_folders = {
        'action', 'asset', 'chr', 'crashdumps', 'cutscene',
        'event', 'expression', 'facegen', 'font', 'map', 'menu',
        'movie', 'msg', 'mtd', 'param', 'parts', 'sfx', 'script',
        'sound', '.smithbox'
    }
    mod_files = {'regulation.bin', 'project.json'}

    # 检查文件夹中是否有特定子文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and item.lower() in mod_folders:
            return True
        if os.path.isfile(item_path) and item.lower() in mod_files:
            return True
    return False


def find_mod_folders(root_dir):
    """查找根目录下所有的MOD文件夹，找到即停止搜索子目录，排除根目录本身"""
    mod_folders = []
    print("找到的MOD文件夹:")

    def traverse_directory(current_dir):
        # 排除modengine2目录
        if 'modengine2' in current_dir:
            return

        # 排除根目录本身
        if current_dir == root_dir:
            # 继续搜索子目录
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    traverse_directory(item_path)
            return

        # 检查当前目录是否为MOD文件夹
        if is_mod_folder(current_dir):
            # 获取相对路径
            rel_path = os.path.relpath(current_dir, root_dir)
            # 获取MOD名称（最后一级目录名）
            mod_name = os.path.basename(current_dir)
            # 转换路径分隔符为双反斜杠
            rel_path = rel_path.replace('\\', '\\\\')
            mod_folders.append({'enabled': True, 'name': mod_name, 'path': rel_path})
            print(f"  {current_dir}")
            return  # 停止搜索子目录

        # 继续搜索子目录
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                traverse_directory(item_path)

    traverse_directory(root_dir)
    print(f"共找到 {len(mod_folders)} 个MOD文件夹")
    return mod_folders


def generate_toml_config(root_dir):
    """生成TOML配置内容"""
    # 查找DLL文件
    dll_files = find_dll_files(root_dir)

    # 查找MOD文件夹
    mod_folders = find_mod_folders(root_dir)

    return dll_files, mod_folders


def format_toml_config(dll_files, mod_folders):
    """按照特定格式生成TOML配置文本"""
    config = "[modengine]\n"
    config += "debug = false\n"
    config += "#DLL配置\n"
    config += "external_dlls = [ \n\n"

    # 添加DLL路径，每个一行
    for dll in dll_files:
        config += f'\t"{dll}",\n'

    config += "\n    ]\n"
    config += "# Mod loader配置\n"
    config += "[extension.mod_loader]\n"
    config += "enabled = true\n"
    config += "loose_params = false\n"
    config += "#文件夹MOD配置\n"
    config += "mods = [\n\n"

    # 添加MOD文件夹配置，每个一行
    for mod in mod_folders:
        config += f'\t{{ enabled = true, name = "{mod["name"]}", path = "{mod["path"]}" }},\n'

    config += "\n]\n"
    config += "[extension.scylla_hide]\n"
    config += "enabled = false\n"

    return config


def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"开始在目录 {script_dir} 中搜索...")

    # 生成配置数据
    dll_files, mod_folders = generate_toml_config(script_dir)

    # 格式化配置文本
    config_text = format_toml_config(dll_files, mod_folders)

    # 写入TOML文件
    config_path = os.path.join(script_dir, 'config_eldenring.toml')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_text)

    print(f"\n配置文件已生成: {config_path}")


if __name__ == "__main__":
    main()    
