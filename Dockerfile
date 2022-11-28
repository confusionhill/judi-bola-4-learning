#
FROM python:3.12.0a2-alpine3.16

#
WORKDIR ./

#
COPY ./requirements.txt ./requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

#
COPY ./ ./

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
