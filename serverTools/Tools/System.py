import shutil
import psutil
import os
import multiprocessing


class System:

    @staticmethod
    def get_used_disk_space(path):
        total, used, free = shutil.disk_usage(path)
        return used

    @staticmethod
    def get_total_disk_space(path):
        total, used, free = shutil.disk_usage(path)
        return total

    @staticmethod
    def get_free_disk_space(path):
        total, used, free = shutil.disk_usage(path)
        return free

    @staticmethod
    def get_cpu_usage(interval=2):
        return psutil.cpu_percent(interval)

    @staticmethod
    def get_used_memory():
        return psutil.virtual_memory().used

    @staticmethod
    def get_total_memory():
        return psutil.virtual_memory().total

    @staticmethod
    def get_load_average():
        one_min, five_min, fifteen_min = os.getloadavg()
        return [round(one_min, 2), round(five_min, 2), round(fifteen_min, 2)]

    @staticmethod
    def get_cpu_count():
        return multiprocessing.cpu_count()
