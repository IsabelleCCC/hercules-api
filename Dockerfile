FROM python:3.10

WORKDIR /hercules

COPY ./requirements.txt /hercules/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /hercules/requirements.txt

COPY ./app /hercules/app

WORKDIR /hercules/app

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
