FROM python:3.10
RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

CMD ["sh", "-c", "python -m flask run --host=0.0.0.0"]