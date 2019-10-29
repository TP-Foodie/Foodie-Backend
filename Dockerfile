FROM python:3

EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/app/src

COPY . .

CMD ["gunicorn", "--workers=5","-b", "0.0.0.0:5000", "app:APP"]
