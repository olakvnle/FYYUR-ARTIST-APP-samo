FROM python:3.8
WORKDIR /app
COPY . /app

RUN chmod +x wait-for

# Create a virtual environment and activate it
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 5000

ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#ENTRYPOINT ["python3", "app.py"]
# C:\Users\HP\Downloads\FYYUR-ARTIST-APP\wait-for
