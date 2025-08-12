from PIL import Image
import os

# 必须由用户输入目录
import os
import sys

# 检查是否有命令行参数
if len(sys.argv) > 1:
    # 使用命令行参数指定的目录
    input_folder = sys.argv[1]
    if not os.path.exists(input_folder):
        print(f"错误：目录 '{input_folder}' 不存在！")
        sys.exit(1)
else:
    # 如果没有提供目录参数，提示用户输入
    print("图片处理工具 - 自动执行重命名 + 调整尺寸并清除EXIF")
    print("=" * 60)
    input_folder = input("请输入要处理的图片目录路径: ").strip()
    
    # 检查目录是否存在
    if not input_folder:
        print("错误：目录路径不能为空！")
        sys.exit(1)
    
    if not os.path.exists(input_folder):
        print(f"错误：目录 '{input_folder}' 不存在！")
        sys.exit(1)

output_folder = os.path.join(input_folder, "resized")  # 用户输入目录下的resized文件夹作为输出目录
target_width = 850                    # 目标宽度

def get_renamed_filenames(directory, keyword):
    """获取重命名后的文件名列表，但不实际重命名原始文件"""
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在！")
        return []
    
    # 获取所有图片文件
    image_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_files.append(filename)
    
    if not image_files:
        print(f"目录 {directory} 中没有找到图片文件！")
        return []
    
    # 按文件名排序，确保重命名顺序一致
    image_files.sort()
    
    # 生成重命名后的文件名映射
    renamed_files = {}
    for i, filename in enumerate(image_files, 1):
        name, ext = os.path.splitext(filename)
        new_filename = f"{keyword}-{i:02d}{ext}"
        renamed_files[filename] = new_filename
    
    print(f"准备处理 {len(image_files)} 张图片...")
    for old_name, new_name in renamed_files.items():
        print(f"重命名：{old_name} → {new_name}")
    
    return renamed_files

def resize_and_clean_images(renamed_files=None):
    """调整图片尺寸并清除EXIF信息"""
    os.makedirs(output_folder, exist_ok=True)  # 如果输出目录不存在则创建

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_path = os.path.join(input_folder, filename)
            try:
                with Image.open(img_path) as img:
                    original_width, original_height = img.size
                    
                    # 判断图片是横版还是竖版
                    if original_width >= original_height:
                        # 横版图片：限制宽度为850px
                        target_size = 850
                        w_percent = target_size / float(original_width)
                        new_width = target_size
                        new_height = int(float(original_height) * w_percent)
                        resize_type = "横版(限制宽度)"
                    else:
                        # 竖版图片：限制高度为850px
                        target_size = 850
                        h_percent = target_size / float(original_height)
                        new_height = target_size
                        new_width = int(float(original_width) * h_percent)
                        resize_type = "竖版(限制高度)"
                    
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # **更高效的EXIF信息删除方法**
                    # 方法1：直接保存时去除EXIF（推荐）
                    
                    # 如果提供了重命名映射，使用新文件名保存
                    if renamed_files and filename in renamed_files:
                        save_filename = renamed_files[filename]
                    else:
                        save_filename = filename
                    
                    save_path = os.path.join(output_folder, save_filename)
                    resized_img.save(save_path, exif=b'')  # 清空EXIF数据
                    
                    # 方法2：如果需要更彻底的清理，可以重新构建图片
                    # data = list(resized_img.getdata())
                    # new_img = Image.new(resized_img.mode, resized_img.size)
                    # new_img.putdata(data)
                    # new_img.save(save_path)
                    
                    print(f"已调整并去除EXIF：{filename} → {save_filename} ({new_width}x{new_height}) [{resize_type}]")
            except Exception as e:
                print(f"处理 {filename} 时出错：{str(e)}")

    print("批量调整完成！所有图片的EXIF信息已清除。")

def main():
    """主函数"""
    print("图片处理工具")
    print("=" * 50)
    print("1. 重命名图片")
    print("2. 调整图片尺寸并清除EXIF")
    print("3. 重命名 + 调整尺寸并清除EXIF")
    print("=" * 50)
    
    choice = input("请选择功能 (1/2/3): ").strip()
    
    if choice == "1":
        keyword = input("请输入重命名关键字: ").strip()
        if keyword:
            rename_images_in_directory(input_folder, keyword)
        else:
            print("关键字不能为空！")
    
    elif choice == "2":
        resize_and_clean_images()
    
    elif choice == "3":
        keyword = input("请输入重命名关键字: ").strip()
        if keyword:
            rename_images_in_directory(input_folder, keyword)
            print("\n" + "=" * 30)
            resize_and_clean_images()
        else:
            print("关键字不能为空！")
    
    else:
        print("无效选择！")

# 直接执行功能3：重命名 + 调整尺寸并清除EXIF
if __name__ == "__main__":
    # 标题已经在目录输入时显示过了，这里只显示关键字输入
    keyword = input("请输入重命名关键字: ").strip()
    if keyword:
        # 获取重命名映射，但不修改原始文件
        renamed_files = get_renamed_filenames(input_folder, keyword)
        if renamed_files:
            print("\n" + "=" * 30)
            # 调整尺寸并保存为重命名后的文件名
            resize_and_clean_images(renamed_files)
    else:
        print("关键字不能为空！")
