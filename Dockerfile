FROM python:3.12-alpine

WORKDIR /blub

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/blub

CMD ["python", "src/main.py"]
