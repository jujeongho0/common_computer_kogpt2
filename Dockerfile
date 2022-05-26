FROM python:3.9.8
WORKDIR /dashboard/
COPY requirements.txt /dashboard/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
