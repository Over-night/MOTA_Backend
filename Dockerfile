FROM python:3.11.0

COPY ./ /home/MOTA/

WORKDIR /home/MOTA/

RUN apt-get update

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["bash", "-c", "python manage.py makemigrations;python manage.py migrate;python manage.py runserver 0.0.0.0:80"]
# CMD ["bash", "-c", "sudo kill -9 $(cat /tmp/mysite.pid) &&  sudo systemctl restart uwsgi"]



# python3.11 manage.py makemigrations
# python3.11 manage.py migrate