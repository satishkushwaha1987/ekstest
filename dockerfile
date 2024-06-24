FROM python3.11

WORKDIR /app

COPY requiretments.txt /app/

RUN pip install -r requiretments.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py" ]