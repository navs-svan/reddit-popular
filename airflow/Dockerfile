# First-time build can take upto 10 mins.

FROM apache/airflow:2.10.1

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt