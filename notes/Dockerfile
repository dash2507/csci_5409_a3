FROM dash2507/flask

WORKDIR /app

ADD . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]