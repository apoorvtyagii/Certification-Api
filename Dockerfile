FROM python:3.6.1-alpine
WORKDIR /API
ADD . /API
CMD ["pip", "uninstall", "MarkupSafe"]
CMD ["pip", "uninstall", "werkzeug"]
RUN pip install -r requirements.txt
CMD ["python", "run.py"]