FROM python:3.12-slim


WORKDIR /app


# system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -c "import easyocr; easyocr.Reader(['en','hi'], gpu=False)"


COPY . .


EXPOSE 8000


CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT