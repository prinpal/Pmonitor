import time

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def timer(base=1, identity: str = "default"):
    def decorator(func):
        total_time = 0
        n = 0

        def wrapper(*args, **kwargs):
            nonlocal n, total_time
            start = time.perf_counter()
            r = func(*args, **kwargs)
            end = time.perf_counter()
            n += base
            total_time += end - start

            print(f"{n} {identity} total time:", total_time)
            print(f"{identity} average time:", total_time / n)
            return r

        return wrapper

    return decorator


def visualize_data(csv_file):
    """
    读取CSV文件并可视化资源消耗情况。

    :param csv_file: CSV文件路径。
    """
    try:
        # 1. 读取数据
        df = pd.read_csv(csv_file)
        if df.empty:
            print(f"CSV文件 '{csv_file}' 为空，无法可视化。")
            return

        # 2. 数据预处理
        # 将时间戳字符串转换为datetime对象，并设为索引
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df.set_index("Timestamp", inplace=True)

        # 3. 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        fig.suptitle(f"Resource Consumption Over Time (from {csv_file})", fontsize=16)

        # 4. 绘制CPU、内存使用率图
        ax1.plot(df.index, df["CPU_Percent"], label="CPU %", color="tab:blue")
        ax1.plot(df.index, df["Memory_Percent"], label="Memory %", color="tab:green")

        ax1.set_ylabel("CPU & Memory Usage (%)")
        ax1.set_ylim(
            0, max(100, df[["CPU_Percent", "Memory_Percent"]].max().max() * 1.1)
        )  # 动态设置Y轴范围
        ax1.legend(loc="upper right")
        ax1.grid(True)

        # 5. 绘制内存使用图
        ax2.plot(df.index, df["Memory_RSS_MB"], label="RSS (Physical)", color="tab:red")
        ax2.plot(
            df.index, df["Memory_VMS_MB"], label="VMS (Virtual)", color="tab:orange"
        )
        ax2.set_ylabel("Memory Usage (MB)")
        ax2.set_xlabel("Time")
        ax2.legend(loc="upper right")
        ax2.grid(True)

        # 6. 格式化X轴时间显示
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        fig.autofmt_xdate()  # 自动旋转日期标签

        plt.tight_layout(rect=(0, 0, 1, 0.96))  # 调整布局为标题留出空间
        plt.show()

    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_file}'。请先运行监控脚本生成数据。")
    except Exception as e:
        print(f"可视化时发生错误: {e}")
