import cv2
import matplotlib.pyplot as plt
import os
import pandas as pd

# ==================== 解决中文显示 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 路径配置 ====================
input_folder = "D:/vs_code_2026/figure/"
output_folder = "D:/vs_code_2026/output/"
slice_folder = "D:/vs_code_2026/slices/"
csv_path = "D:/vs_code_2026/图片信息汇总.csv"

# ==================== 功能开关 ====================
RUN_SHOW_GRAY = False      # 显示单张灰度图（弹窗）
RUN_BATCH_PRINT = False    # 批量打印图片尺寸
RUN_SAVE_GRAY = False      # 批量保存灰度图到 output
RUN_GENERATE_CSV = False   # 生成 CSV 汇总表格
RUN_SLICE = True           # 切片（当前开）
RUN_GENERATE_JSON = True   # 生成 JSON 标注文件（当前开）
RUN_NEGATIVE = True        #让所有切片图变成黑白反转（负片效果）（当前开）
RUN_HISTOGRAM = True       #画出睡莲（负片）的亮度直方图（当前开）

# ==================== 功能1：显示单张灰度图 ====================
if RUN_SHOW_GRAY:
    img = cv2.imread("D:/vs_code_2026/figure/artificial_flower.jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.subplot(1,2,1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('原图')
    plt.subplot(1,2,2)
    plt.imshow(gray_img, cmap='gray')
    plt.title('灰度图')
    plt.show()

# ==================== 功能2：批量打印尺寸 ====================
if RUN_BATCH_PRINT:
    print("开始批量处理图片...")
    for file_name in os.listdir(input_folder):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(input_folder, file_name)
            img = cv2.imread(img_path)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                print(f"✅ {file_name} 处理完成，尺寸: {img.shape}")
            else:
                print(f"❌ {file_name} 读取失败，跳过")
    print("批量处理结束！")

# ==================== 功能3：批量保存灰度图 ====================
if RUN_SAVE_GRAY:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file_name in os.listdir(input_folder):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(input_folder, file_name)
            img = cv2.imread(img_path)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray_name = "gray_" + file_name
                gray_path = os.path.join(output_folder, gray_name)
                cv2.imwrite(gray_path, gray)
                print(f"✅ 已保存: {gray_name}")

# ==================== 功能4：生成CSV汇总 ====================
if RUN_GENERATE_CSV:
    data_list = []
    target_folder = output_folder if os.path.exists(output_folder) else input_folder
    for file_name in os.listdir(target_folder):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(target_folder, file_name)
            img = cv2.imread(img_path)
            if img is not None:
                h, w, c = img.shape
                data_list.append({
                    '文件名': file_name,
                    '宽度': w,
                    '高度': h,
                    '通道数': c,
                    '总像素数': w * h
                })
    if data_list:
        df = pd.DataFrame(data_list)
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV已生成: {csv_path}")

# ==================== 功能5：切片 ====================
if RUN_SLICE:
    def slice_image(image_path, output_slice_folder, rows=2, cols=2):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return
        h, w = img.shape
        slice_h = h // rows
        slice_w = w // cols
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        for i in range(rows):
            for j in range(cols):
                y_start = i * slice_h
                y_end = (i + 1) * slice_h
                x_start = j * slice_w
                x_end = (j + 1) * slice_w
                slice_img = img[y_start:y_end, x_start:x_end]
                slice_name = f"{base_name}_slice_{i}_{j}.jpg"
                slice_path = os.path.join(output_slice_folder, slice_name)
                cv2.imwrite(slice_path, slice_img)
                print(f"   ✅ 已保存切片: {slice_name}")

    if not os.path.exists(slice_folder):
        os.makedirs(slice_folder)
    
    # 确定从哪个文件夹切片（优先用 output，没有就用 input）
    source_folder = output_folder if os.path.exists(output_folder) else input_folder
    print(f"🔪 开始切片，图片来源: {source_folder}")
    for file_name in os.listdir(source_folder):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(source_folder, file_name)
            print(f"🔪 正在切片: {file_name}")
            slice_image(img_path, slice_folder, rows=2, cols=2)
    print(f"✅ 所有切片完成！去 {slice_folder} 看看吧！")


# ==================== 功能6：生成 JSON 标注文件 ====================
if RUN_GENERATE_JSON:
    import json
    # 从切片文件名提取标签（按文件名关键词分类）
    label_map = {
        "flower": "花",
        "book": "书",
        "tiexianlian": "铁线莲",
        "water_lily": "睡莲",
        "tree": "树"
    }
    
    json_data = []
    for file_name in os.listdir(slice_folder):
        if file_name.endswith('.jpg'):
            img_path = os.path.join(slice_folder, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                h, w = img.shape
                # 根据文件名推断标签
                label = "未知"
                for key, value in label_map.items():
                    if key in file_name.lower():
                        label = value
                        break
                
                json_data.append({
                    "文件名": file_name,
                    "路径": img_path,
                    "宽度": w,
                    "高度": h,
                    "标签": label
                })

    # 保存为 JSON
    json_path = "D:/vs_code_2026/标注数据.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 标注文件已生成: {json_path}")
    print(f"   共标注 {len(json_data)} 张切片")


 # ==================== 功能7：负片效果（黑白反转） ==================== 
if RUN_NEGATIVE:
    neg_folder = "D:/vs_code_2026/negative/"
    if not os.path.exists(neg_folder):
        os.makedirs(neg_folder)
    
    for file_name in os.listdir(slice_folder):
        if file_name.endswith('.jpg'):
            img = cv2.imread(os.path.join(slice_folder, file_name), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                neg = 255 - img
                cv2.imwrite(os.path.join(neg_folder, "neg_" + file_name), neg)
                print(f"✅ 负片已生成: neg_{file_name}")
    print(f"所有负片已保存到 {neg_folder}")
# ==================== 功能8：睡莲（负片）直方图 ====================
if RUN_HISTOGRAM:
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 找一张睡莲的切片
    sample_path = None
    for f in os.listdir(slice_folder):
        if 'water_lily' in f:
            sample_path = os.path.join(slice_folder, f)
            break
    
    if sample_path:
        img = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
        neg = 255 - img
        
        plt.figure(figsize=(10,4))
        plt.subplot(1,2,1)
        plt.imshow(neg, cmap='gray')
        plt.title('负片（水墨风）')
        plt.axis('off')
        
        plt.subplot(1,2,2)
        plt.hist(neg.ravel(), bins=256, range=[0,256], color='gray')
        plt.title('像素亮度分布')
        plt.xlabel('亮度值 (0=黑, 255=白)')
        plt.ylabel('像素数量')
        plt.axvline(neg.mean(), color='red', linestyle='--', label=f'均值: {neg.mean():.1f}')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        print(f"✅ 睡莲负片平均亮度: {neg.mean():.1f} (偏亮 → 水墨感)")