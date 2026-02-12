FROM python:3.12-slim

WORKDIR /app

# Install runtime deps from your local source (no uv)
COPY pyproject.toml README.md /app/
COPY pharo_smalltalk_interop_mcp_server /app/pharo_smalltalk_interop_mcp_server

RUN pip install --no-cache-dir .

ENV PHARO_SIS_URL=http://host.docker.internal:8086

ENTRYPOINT ["pharo-smalltalk-interop-mcp-server"]