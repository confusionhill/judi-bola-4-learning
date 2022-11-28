#
FROM python:3.9-alpine3.15

#
WORKDIR ./

#
COPY ./requirements.txt ./requirements.txt

#

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

#
COPY ./ ./

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
