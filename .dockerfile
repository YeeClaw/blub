FROM python:3.12-alpine

WORKDIR /blub

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add nano

COPY . .

ENV PYTHONPATH=/blub

# The only way I can get this to work is to copy (and remove) the entrypoint script to the root directory
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN rm entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]