pip install uv
uv build
uv run -m pypi_attestations sign dist/*
uv publish
