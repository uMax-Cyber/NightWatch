FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN find scripts/ -name "*.py" -exec chmod +x {} + 2>/dev/null; \
    find scripts/ -name "*.sh" -exec chmod +x {} + 2>/dev/null; true
CMD ["echo", "See README.md for usage"]
