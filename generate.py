import requests
import re

# 配置信息
HTML_OUTPUT_FILE = "link.html"  # HTML输出文件名

# 获取文件夹列表
def get_folder_content(parent_path, ALIST_URL):
    url = f"{ALIST_URL}/api/fs/list"
    params = {
        "path": f"/{parent_path}"
    }
    response = requests.get(url, params=params)
    
    try:
        return response.json()["data"]["content"]
    except (requests.exceptions.JSONDecodeError, KeyError):
        print("无法解析文件列表，请检查目标路径是否正确或网站是否支持匿名访问。")
        return []

# 递归遍历文件夹
def traverse_folders(path, ALIST_URL):
    content = get_folder_content(path, ALIST_URL)
    html_links = []  # 用于存储HTML格式的链接
    
    for item in content:
        full_path = f"{path}/{item['name']}"
        if item["is_dir"]:
            print(f"进入文件夹: {full_path}")
            traverse_folders(full_path, ALIST_URL)
        else:
            # 提取链接名字并生成HTML格式
            filename = re.search(r'.*/([^/]+)$', f"{ALIST_URL}/d/{full_path}").group(1)
            html_link = f'<a href="{ALIST_URL}/d/{full_path}">{filename}</a></br>'
            html_links.append(html_link)
    
    # 将HTML链接写入文件
    if html_links:
        with open(HTML_OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write('\n'.join(html_links) + '\n')

# 主函数
def main():
    # 提示用户输入网站地址
    ALIST_URL = input("请输入你要遍历的网站(末尾不要加上“/”符号): ").strip()
    
    # 提示用户输入文件夹名称
    folder_input = input("请输入你要遍历的文件夹(填目录名字无需“/”符号，不填默认遍历根目录): ").strip()
    TARGET_FOLDER = folder_input if folder_input else ""
    
    print(f"开始遍历：{TARGET_FOLDER}")
    traverse_folders(TARGET_FOLDER, ALIST_URL)
    print(f"\n遍历完成！HTML格式链接已保存到 {HTML_OUTPUT_FILE}")

# 运行
if __name__ == "__main__":
    main()
