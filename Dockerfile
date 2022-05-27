FROM python:3.9.8

EXPOSE 8501

WORKDIR /app

RUN pip install --upgrade pip 
RUN pip install protobuf==3.20.1
RUN pip install streamlit
RUN pip install streamlit_chat
RUN pip install transformers

COPY . /app
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
