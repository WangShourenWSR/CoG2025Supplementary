import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 这里收集了一些之前提到的颜色，包含了 teal, orange, purple, green, gray 等
colors = [
    ("#1abc9c",  "Turquoise"),
    ("#16a085",  "Green Sea"),
    ("#12b5cb",  "Teal #12b5cb"),
    ("#48C9B0",  "Light Turquoise"),
    ("#3498db",  "Dodger Blue"),
    ("#2980b9",  "Belize Hole"),
    ("#2ecc71",  "Emerald"),
    ("#27ae60",  "Nephritis"),
    ("#e67e22",  "Carrot"),
    ("#d35400",  "Pumpkin"),
    ("#e74c3c",  "Alizarin"),
    ("#e8710a",  "Orange #e8710a"),
    ("#9b59b6",  "Amethyst"),
    ("#8e44ad",  "Wisteria"),
    ("#7f8c8d",  "Concrete"),
    ("#34495e",  "Wet Asphalt"),
    ("#2c3e50",  "Midnight Blue"),
    ("#f1c40f",  "Sun Flower"),
]

plt.figure(figsize=(6, 8))

# 依次绘制一个个矩形色块，并在右侧标注颜色名称和Hex值
for i, (hex_code, name) in enumerate(colors):
    # 画一个矩形色块：左下角 (0, i)，宽度=2，高度=0.8
    rect = patches.Rectangle((0, i), 2, 0.8, color=hex_code)
    plt.gca().add_patch(rect)
    
    # 在矩形右侧显示文字
    plt.text(2.3, i + 0.4, f"{name} ({hex_code})", va='center', fontsize=10)

# 调整坐标范围，翻转 y 轴让第一个颜色在最上方（可根据喜好决定是否翻转）
plt.xlim(0, 6)
plt.ylim(len(colors), 0)  # 让 y 轴从上到下递增
plt.axis('off')
plt.title("Example Color Palette", fontsize=14)
plt.show()
