FROM python:3.8-slim

WORKDIR /src/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/chinarv" ]

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "src.main:app"]

CMD ["python", "src/main.py"]