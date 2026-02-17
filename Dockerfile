FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl xz-utils ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    -o /tmp/ffmpeg.tar.xz \
    && tar -xJf /tmp/ffmpeg.tar.xz -C /tmp \
    && mv /tmp/ffmpeg-*-static/ffmpeg /usr/local/bin/ffmpeg \
    && mv /tmp/ffmpeg-*-static/ffprobe /usr/local/bin/ffprobe \
    && chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe \
    && rm -rf /tmp/ffmpeg*

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -r requirements.txt

# start dosyası varsa: CRLF temizle + çalıştırılabilir yap
RUN if [ -f start ]; then sed -i 's/\r$//' start && chmod +x start; fi

CMD ["bash", "-lc", "if [ -f ./start ]; then ./start; else python3 -m Pandamusic; fi"]
