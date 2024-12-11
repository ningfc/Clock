
import platform

# 获取当前操作系统
system_name = platform.system()
print(system_name)

import tkinter as tk
if system_name == "Darwin":
    from tkmacosx import Button
import time
import math

class TimerApp:
    def __init__(self, root):
        # 禁止水平和垂直方向的缩放
        root.resizable(width=False, height=False)
        # 设置窗口置顶
        root.attributes("-topmost", True)
        
        self.root = root
        self.root.title("计时器")
        self.canvas_size = 600
        self.circle_radius = 225
        self.center_x = self.canvas_size // 2
        self.center_y = self.canvas_size // 2

        # 创建画布
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black")
        self.canvas.pack()
        
        self.draw_circle()

        # 时间标签 (显示在圆环中心)
        self.time_label = self.canvas.create_text(
            self.center_x, self.center_y, text="00:00:00.00", font=("Helvetica", 50), fill="green"
        )

        # 小圆的初始位置
        angle_radians = math.radians(0 - 90)  # 转换为弧度并调整角度以零点朝上
        dot_x = self.center_x + self.circle_radius * math.cos(angle_radians)
        dot_y = self.center_y + self.circle_radius * math.sin(angle_radians)
        self.millisecond_line = self.canvas.create_line(
            self.center_x, self.center_y,
            dot_x, dot_y,
            fill="red"
        )
        self.millisecond_dot = self.canvas.create_oval(
            dot_x - 5, dot_y - 5,
            dot_x + 5, dot_y + 5,
            fill="red"
        )

        # 初始化计时器
        self.running = False
        self.start_time = None
        self.update_clock()

        # 添加按钮
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        if system_name == "Darwin":
            self.start_button = Button(button_frame,
                text="启动", font=("Helvetica", 16), 
                width=150, height=50, 
                bg='black', 
                fg='gray', 
                command=self.start_timer)

            self.start_button.pack(side=tk.LEFT, padx=15)

            self.reset_button = Button(button_frame, 
                text="重置", font=("Helvetica", 16), 
                width=150, height=50, 
                bg='black', 
                fg='gray', 
                command=self.reset_timer
            )
            self.reset_button.pack(side=tk.LEFT, padx=15)
        else: #elif system_name == "Windows":
            self.start_button = tk.Button(button_frame,
                text="启动", font=("Helvetica", 16), 
                width=10, height=2, 
                bg='black', 
                fg='gray', 
                command=self.start_timer)

            self.start_button.pack(side=tk.LEFT, padx=15)

            self.reset_button = tk.Button(button_frame, 
                text="重置", font=("Helvetica", 16), 
                width=10, height=2, 
                bg='black', 
                fg='gray', 
                command=self.reset_timer
            )
            self.reset_button.pack(side=tk.LEFT, padx=15)

    def draw_circle(self):
        self.canvas.delete("all")
        radius = self.circle_radius  # 圆半径

        # 绘制秒刻度
        pointLentgh = 10
        for i in range(10):  # 50 个刻度，每 0.1 秒一个
            angle = 360 * i / 10 - 90
            length = pointLentgh * 2 if i % 2 == 0 else pointLentgh
            if i % 2 == 0:
                x0 = self.center_x + (radius - length - pointLentgh) * math.cos(math.radians(angle))
                y0 = self.center_y + (radius - length - pointLentgh) * math.sin(math.radians(angle))
                self.time_label = self.canvas.create_text(
                    x0, y0, text=str(i//2), font=("Helvetica", 25), fill="green"
                )

            x1 = self.center_x + (radius - length) * math.cos(math.radians(angle))
            y1 = self.center_y + (radius - length) * math.sin(math.radians(angle))
            x2 = self.center_x + radius * math.cos(math.radians(angle))
            y2 = self.center_y + radius * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill="lightgray", width=1)


        # 定义圆心和圆形范围
        self.circle = self.canvas.create_oval(
            self.center_x - self.circle_radius, 
            self.center_y - self.circle_radius,
            self.center_x + self.circle_radius, 
            self.center_y + self.circle_radius,
            outline="gray", width=2
        )

        
    def update_clock(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
            seconds = int(elapsed_time) % 60
            minutes = (int(elapsed_time) // 60) % 60
            hours = (int(elapsed_time) // 3600) % 24

            # 更新时间显示
            time_text = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"
            self.canvas.itemconfig(self.time_label, text=time_text)

            # 计算小圆位置（5秒一圈）
            angle = ((elapsed_time % 5) / 5) * 360  # 5秒对应 360 度
            angle_radians = math.radians(angle - 90)  # 转换为弧度并调整角度以零点朝上
            dot_x = self.center_x + self.circle_radius * math.cos(angle_radians)
            dot_y = self.center_y + self.circle_radius * math.sin(angle_radians)

            # 更新小圆位置
            self.canvas.coords(
                self.millisecond_line,
                self.center_x, self.center_y,
                dot_x, dot_y,
            )
            self.canvas.coords(
                self.millisecond_dot,
                dot_x - 5, dot_y - 5,
                dot_x + 5, dot_y + 5
            )

        # 每隔 10 毫秒更新一次
        self.root.after(10, self.update_clock)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() if self.start_time is None else self.start_time

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.canvas.itemconfig(self.time_label, text="00:00:00.00")
        angle_radians = math.radians(0 - 90)  # 转换为弧度并调整角度以零点朝上
        dot_x = self.center_x + self.circle_radius * math.cos(angle_radians)
        dot_y = self.center_y + self.circle_radius * math.sin(angle_radians)
        self.canvas.coords(
            self.millisecond_line,
            self.center_x, self.center_y,
            dot_x, dot_y,
        )
        self.canvas.coords(
            self.millisecond_dot,
            dot_x - 5, dot_y - 5,
            dot_x + 5, dot_y + 5
        )

# 创建主窗口
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
