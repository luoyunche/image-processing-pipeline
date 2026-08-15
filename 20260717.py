import cv2
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
# 解决中文显示问题（加上这三行）

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# ======先处理一张图片======#
# 1. 读入图片（这就是OpenCV的入口）
img = cv2.imread("D:/vs_code_2026/figure/artificial_flower.jpg")  # 路径别带中文

# 2. 把彩图变成灰度图（这就是OpenCV最核心的算法）
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. 展示出来（左边原图，右边灰度图）
plt.subplot(1,2,1), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('原图')
plt.subplot(1,2,2), plt.imshow(gray_img, cmap='gray'), plt.title('灰度图')
plt.show()


# ======批量处理======#
import os

folder_path = "D:/vs_code_2026/figure/"
print("开始批量处理图片...")
for file_name in os.listdir(folder_path): #for数据遍历 #os.listdir()文件扫描
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(folder_path, file_name)
        img = cv2.imread(img_path)
        if img is not None:  # 防止读取失败
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #cv2.imread() → cv2.cvtColor() = 数据清洗/转换
            print(f"✅ {file_name} 处理完成，尺寸: {img.shape}")
        else:   
            print(f"❌ {file_name} 读取失败，跳过")
print("批量处理结束！")


# ======自动创建包含全部灰度图片的文件夹======#
# 原图文件夹
input_folder = "D:/vs_code_2026/figure/"
# 新建一个输出文件夹（代码会自动创建）
output_folder = "D:/vs_code_2026/output/"

# 如果输出文件夹不存在，就自动创建一个
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(input_folder, file_name)
        img = cv2.imread(img_path)
        
        if img is not None:
            # 转灰度
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 保存灰度图（在原文件名前加 'gray_'）
            gray_name = "gray_" + file_name
            gray_path = os.path.join(output_folder, gray_name)
            cv2.imwrite(gray_path, gray) #数据持久化
            
            print(f"✅ 已保存: {gray_name}")
        else:
            print(f"❌ 读取失败: {file_name}")

print("所有图片处理完毕！去 output 文件夹看看吧！")


# ====== 表格，记录每张图的文件名、尺寸、像素总数等信息======#
import pandas as pd
# 收集图片信息
data_list = []
output_folder = "D:/vs_code_2026/output/"

for file_name in os.listdir(output_folder):
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(output_folder, file_name)
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

# 转成 DataFrame 并保存为 CSV
df = pd.DataFrame(data_list) #数据目录/数据湖元数据管理
df.to_csv("D:/vs_code_2026/图片信息汇总.csv", index=False, encoding='utf-8-sig')
print("✅ CSV 表格已生成！去 D:/vs_code_2026/ 看看 图片信息汇总.csv")


# ====== 图像切片：把 output 文件夹里的每张灰度图切成 4 块 ======#
def slice_image(image_path, output_slice_folder, rows=2, cols=2):
    """
    把一张图片切成 rows x cols 块
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 直接读灰度图
    if img is None:
        return
    h, w = img.shape
    slice_h = h // rows
    slice_w = w // cols

    base_name = os.path.splitext(os.path.basename(image_path))[0]  # 去掉扩展名
    for i in range(rows):
        for j in range(cols):
            # 计算切片位置
            y_start = i * slice_h
            y_end = (i + 1) * slice_h
            x_start = j * slice_w
            x_end = (j + 1) * slice_w
            
            # 切出小块
            slice_img = img[y_start:y_end, x_start:x_end]
            
            # 保存
            slice_name = f"{base_name}_slice_{i}_{j}.jpg"
            slice_path = os.path.join(output_slice_folder, slice_name)
            cv2.imwrite(slice_path, slice_img)
            print(f"   ✅ 已保存切片: {slice_name}")
# 创建切片输出文件夹
slice_folder = "D:/vs_code_2026/slices/"
if not os.path.exists(slice_folder):
    os.makedirs(slice_folder)
    
print("\n开始切片处理...")
for file_name in os.listdir(output_folder):
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(output_folder, file_name)
        print(f"🔪 正在切片: {file_name}")
        slice_image(img_path, slice_folder, rows=2, cols=2)

print(f"✅ 所有切片完成！去 {slice_folder} 看看吧！")
