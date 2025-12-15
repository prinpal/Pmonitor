import csv
import os
import time
from datetime import datetime

import psutil


class ResourceMonitor:
    """
    一个持续监控指定进程CPU和内存消耗，并将数据持久化到CSV的模块。
    """

    def __init__(self, pid, output_file="resource_log.csv", interval=1.0):
        """
        初始化监控器。

        :param pid: 要监控的进程ID。
        :param output_file: 输出CSV文件的路径。
        :param interval: 监控间隔（秒）。
        """
        self.pid = pid
        self.interval = interval
        self.output_file = output_file
        self._running = False

        # 尝试附加到进程
        try:
            self.process = psutil.Process(pid)
            print(f"成功附加到进程 PID: {pid} ({self.process.name()})")
        except psutil.NoSuchProcess:
            raise ValueError(f"找不到PID为 {pid} 的进程。")
        except psutil.AccessDenied:
            raise ValueError(f"没有权限访问PID为 {pid} 的进程。")

        # 准备CSV文件头
        self._prepare_csv()

    def _prepare_csv(self):
        """准备CSV文件，如果不存在则创建并写入表头。"""
        file_exists = os.path.isfile(self.output_file)
        # 使用追加模式 'a'，如果文件不存在会自动创建
        with open(self.output_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists or os.path.getsize(self.output_file) == 0:
                writer.writerow(
                    [
                        "Timestamp",
                        "CPU_Percent",
                        "Memory_Percent",
                        "Memory_RSS_MB",
                        "Memory_VMS_MB",
                    ]
                )

    def _monitor_loop(self):
        """监控循环，在后台线程中运行。"""
        print(f"监控开始，数据将每 {self.interval} 秒记录到 '{self.output_file}'")
        while self._running:
            try:
                # 获取时间戳
                timestamp = datetime.now().isoformat()

                met = self.process.as_dict(
                    ["pid", "cpu_percent", "memory_percent", "memory_info"]
                )
                # 获取CPU使用率（非阻塞）
                cpu_percent = met["cpu_percent"] / psutil.cpu_count()

                # 获取内存信息
                mem_percent = met["memory_percent"]
                mem_info = met["memory_info"]
                mem_rss_mb = mem_info.rss / (1024 * 1024)  # 物理内存
                mem_vms_mb = mem_info.vms / (1024 * 1024)  # 虚拟内存

                # 写入CSV
                with open(self.output_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            timestamp,
                            f"{cpu_percent:.2f}",
                            f"{mem_percent:.2f}",
                            f"{mem_rss_mb:.2f}",
                            f"{mem_vms_mb:.2f}",
                        ]
                    )

            except psutil.NoSuchProcess:
                print(f"\n进程 {self.pid} 已结束，停止监控。")
                self.stop()  # 进程已退出，自动停止监控
                break
            except KeyboardInterrupt:
                print("\n用户中断监控。")
                self.stop()
                break
            except Exception as e:
                print(f"\n监控时发生错误: {e}")
                break

            time.sleep(self.interval)

    def start(self):
        """启动监控线程。"""
        if self._running:
            print("监控已在运行中。")
            return

        self._running = True
        self._monitor_loop()

    def stop(self):
        """停止监控线程。"""
        if not self._running:
            print("监控未在运行。")
            return

        print("\n正在停止监控...")
        self._running = False
        print("监控已停止。")
