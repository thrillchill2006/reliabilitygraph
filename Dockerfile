FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY data/corpus/manifest.json data/corpus/passages.json data/corpus/sections.json ./data/corpus/
COPY scripts/build_index.py ./scripts/build_index.py
RUN pip install --no-cache-dir uv==0.6.14 && \
    uv pip install --system ".[app]" && \
    python scripts/build_index.py

COPY src/reliabilitygraph ./src/reliabilitygraph
EXPOSE 8000
ENV RELIABILITYGRAPH_KILL_SWITCH=false
CMD ["uvicorn", "reliabilitygraph.api:app", "--host", "0.0.0.0", "--port", "8000"]
