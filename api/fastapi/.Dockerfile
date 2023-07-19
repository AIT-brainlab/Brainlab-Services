FROM python:3.9.17-bookworm

# You do not need to expose 443.
# The TLS will be handled by `traefik`
EXPOSE 80

RUN pip3 install --upgrade pip
# Specify the version so every build is consistent

# Let's install the FastAPI first.
RUN pip3 install fastapi==0.100.0
RUN pip3 install "uvicorn[standard]==0.23.1"

# Now you build your environment here

CMD tail -f /dev/null