FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update && \
      apt-get -y install sudo

# Copy dependecies and install them as root
COPY install_dependencies.sh install_dependencies.sh
RUN sh install_dependencies.sh

# Copy drivers and install them as root
COPY driver_odbc_linux.sh driver_odbc_linux.sh
RUN sh driver_odbc_linux.sh

COPY . .



CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]