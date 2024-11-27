FROM python:3.9

# Обновляем и улучшаем систему
RUN apt-get update && apt-get install -y netcat-openbsd
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY ./requirements.txt ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Собираем статику с флагом --noinput

# Копируем оставшиеся файлы проекта
COPY ./ ./
RUN mkdir -p /app/static
RUN python3 manage.py collectstatic --noinput

# Указываем команду для запуска приложения
CMD ["gunicorn", "parserBuildTools.wsgi:application", "--bind", "0.0.0.0:8000"]
