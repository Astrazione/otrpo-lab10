import logging
from prometheus_client import start_http_server, Gauge
import psutil
import os
from dotenv import load_dotenv
import asyncio


class MetricsCollector:
    cpu_usage = Gauge("cpu_usage", "Usage of CPU cores", ["core"])
    memory_total = Gauge("memory_total", "Total memory in the system")
    memory_used = Gauge("memory_used", "Used memory in the system")
    disk_total = Gauge("disk_total", "Total disk space")
    disk_used = Gauge("disk_used", "Used disk space")
    collecting_task = None

    async def start_collecting(self):
        logging.info('Запуск сборщика метрик')
        self.collecting_task = asyncio.create_task(self.collecting_loop())
        await self.collecting_task

    def stop_collecting(self):
        self.collecting_task.cancel()

    async def collecting_loop(self):
        try:
            while True:
                self.collect_metrics()
                await asyncio.sleep(5)  # Сбор метрик каждые 5 секунд
        except asyncio.CancelledError:
            logging.info("Сбор метрик завершён!")

    def collect_metrics(self):
        self.get_cpu_info()
        self.get_memory_info()
        self.get_disk_info()

    def get_cpu_info(self):
        for i, perc in enumerate(psutil.cpu_percent(percpu=True)):
            self.cpu_usage.labels(core=f"core_{i}").set(perc)

    def get_memory_info(self):
        mem = psutil.virtual_memory()
        self.memory_total.set(mem.total)
        self.memory_used.set(mem.used)

    def get_disk_info(self):
        disk = psutil.disk_usage('/')
        self.disk_total.set(disk.total)
        self.disk_used.set(disk.used)


def load_env():
    if load_dotenv('params.env'):
        logging.info('Переменные среды загружены')
    else:
        logging.error('Ошибка загрузки параметров среды')


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    load_env()

    host = os.getenv("EXPORTER_HOST", "0.0.0.0")
    port = int(os.getenv("EXPORTER_PORT", "8000"))

    logging.info('Запуск сервера')
    start_http_server(port, addr=host)
    print(f"Сервер запущен: http://{host}:{port}")

    collector = MetricsCollector()
    task = asyncio.create_task(collector.start_collecting())
    try:
        await task
    except asyncio.CancelledError:
        logging.info("Завершение работы")


if __name__ == "__main__":
    asyncio.run(main())
