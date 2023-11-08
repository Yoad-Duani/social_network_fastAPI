FROM python:3.9

RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall fastapi_keycloak -y 

# RUN git clone https://github.com/Yoad-Duani/fastapi-keycloak-yoad.git /usr/src/fastapi-keycloak-yoad

# RUN python /usr/src/fastapi-keycloak-yoad/setup.py install

# RUN pip install /usr/src/fastapi-keycloak-yoad

COPY . .

RUN pip install "git+https://github.com/Yoad-Duani/fastapi-keycloak-yoad.git"

EXPOSE 8002

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8002"]