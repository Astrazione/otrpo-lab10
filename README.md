## Описание

Приложение-экспортер на языке программирования Python. Собирает для Prometheus информацию
об использовании ядер процессора, общее и используемое количество оперативной памяти и дискового пространства

## Подготовка к запуску
Необходимо установить следующие пакеты командой
```
pip install prometheus-client psutil python-dotenv
```
В файле `params.env` необходимо указать переменные окружения
`EXPORTER_HOST`, `EXPORTER_PORT`

В конфиге `prometheus.yml` необходимо добавить в `scrape_configs`:
```yml
- job_name: "metrics"
  static_configs:
  - targets: ["localhost:8000"]
```

В Grafana нужно импортировать `dashboard` и настроить `datasource`

## Запросы на PromQL

Процент загрузки процессора: `avg(cpu_usage{job="metrics"})`

Количество потоков процессора: `count(cpu_usage{job="metrics"})`

Всего и используемая оперативная память (в байтах): `memory_total{job="metrics"}` и `memory_used{job="metrics"}`

Всего и используемое дисковое пространство (в байтах): `disk_total{job="metrics"}` и `disk_used{job="metrics"}`