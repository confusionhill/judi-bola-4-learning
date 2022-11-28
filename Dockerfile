#
FROM python:3.11.0-buster

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
