FROM python:3

EXPOSE 5000

COPY requirements.txt ./
COPY test ./usr/app/test/
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/app/src

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:APP"]
