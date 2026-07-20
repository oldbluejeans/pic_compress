# Image Compress Tool
# Copyright (c) 2026 
# Released under the MIT License.
# import os
from PIL import Image
from io import BytesIO

# ===================== 配置区 =====================
MAX_SIZE_KB = 100             # 单张图片最大100KB
MIN_QUALITY = 20              # 最低画质下限
# ==================================================

# 自动获取当前Windows登录用户名
user_name = os.environ.get("USERNAME")
# 拼接路径
INPUT_FOLDER = rf"C:\Users\{user_name}\Desktop\temp\old"
OUTPUT_FOLDER = rf"C:\Users\{user_name}\Desktop\temp\new"

# 标记是否本次新建了任意文件夹
need_prompt = False
if not os.path.exists(INPUT_FOLDER):
    os.makedirs(INPUT_FOLDER)
    need_prompt = True
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    need_prompt = True

# 只要有文件夹是刚创建的，提示用户放入图片后退出
if need_prompt:
    print(f"检测到输入和输出目录不存在，已自动创建目录：")
    print(f"原图目录：{INPUT_FOLDER}")
    print(f"输出目录：{OUTPUT_FOLDER}")
    print(f"\n请将需要转换的文件copy到{INPUT_FOLDER}目录，copy完成后再次执行该脚本")
    input("\n按回车键退出...")
    exit()

# 两个文件夹原本就存在，直接执行压缩逻辑
print("检测到old、new目录均已存在，开始执行图片压缩...")

def compress_image(file_path, output_path, max_kb):
    """单张图片循环压缩至指定大小以内"""
    img = Image.open(file_path)
    quality = 95
    max_bytes = max_kb * 1024

    while quality >= MIN_QUALITY:
        buffer = BytesIO()
        # PNG转RGB后保存为JPG提升压缩率
        if img.format == "PNG":
            img = img.convert("RGB")
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        file_size = buffer.tell()

        if file_size <= max_bytes:
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            print(f"✅ 完成 | {os.path.basename(file_path)} | 画质:{quality} | 大小:{round(file_size/1024,2)}KB")
            break
        quality -= 5
    else:
        print(f"⚠️ {os.path.basename(file_path)} 降至最低画质仍超过{max_kb}KB")

def batch_compress(input_dir, output_dir):
    # 遍历图片文件
    for filename in os.listdir(input_dir):
        suffix = filename.lower().split(".")[-1]
        if suffix not in ["jpg", "jpeg", "png"]:
            continue
        src_path = os.path.join(input_dir, filename)
        out_name = os.path.splitext(filename)[0] + ".jpg"
        out_path = os.path.join(output_dir, out_name)
        compress_image(src_path, out_path, MAX_SIZE_KB)

if __name__ == "__main__":
    batch_compress(INPUT_FOLDER, OUTPUT_FOLDER)
    print("\n🎉 所有图片压缩任务执行完毕！")
    input("\n按回车关闭窗口...")