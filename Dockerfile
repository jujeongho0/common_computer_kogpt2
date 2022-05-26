FROM python:3.7-stretch
WORKDIR /dashboard/
COPY requirements.txt /dashboard/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
