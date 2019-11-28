FROM hsb-log

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# add startup script
ADD entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
