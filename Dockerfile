FROM python:3.10-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

