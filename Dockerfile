FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./user_by_distance.py" ]
ENTRYPOINT ["python", "./user_by_distance.py"]
