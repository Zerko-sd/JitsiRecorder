FROM python:3.11-slim

# Install system deps required by Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    libxdamage1 \
    libxfixes3 \
    libxext6 \
    libx11-xcb1 \
    fonts-liberation \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Playwright
RUN pip install --no-cache-dir playwright

# Install Chromium for Playwright
RUN playwright install chromium

COPY recorder.py .

CMD ["python", "recorder.py"]
