FROM python:3.10

# Tạo thư mục làm việc
WORKDIR /app

# Cài các thư viện hệ thống để TensorFlow hoạt động
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libffi-dev \
    libssl-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài thư viện Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8005

CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]
