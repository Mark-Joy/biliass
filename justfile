VERSION := `poetry run python -c "import sys; from biliass import __version__ as version; sys.stdout.write(version)"`

install:
  poetry install

test:
  just gen-test-files
  poetry run pytest
  just clean

fmt:
  poetry run isort .
  poetry run black .

fmt-docs:
  prettier --write '**/*.md'

build:
  poetry build

publish:
  touch biliass/py.typed
  poetry publish --build
  git tag "v{{VERSION}}"
  git push --tags
  just clean-builds

clean:
  find . -name "*.xml" -print0 | xargs -0 rm -f
  find . -name "*.ass" -print0 | xargs -0 rm -f
  find . -name "*.pb" -print0 | xargs -0 rm -f
  find . -name "*.m4s" -print0 | xargs -0 rm -f
  find . -name "*.mp4" -print0 | xargs -0 rm -f
  find . -name "*.aac" -print0 | xargs -0 rm -f
  find . -name "*.xml" -print0 | xargs -0 rm -f
  find . -name "*.srt" -print0 | xargs -0 rm -f
  find . -name "*.ass" -print0 | xargs -0 rm -f
  rm -rf .pytest_cache

clean-builds:
  rm biliass/py.typed
  rm -rf biliass/biliass.pyi
  rm -rf .mypy_cache/
  rm -rf **/__pycache__
  rm -rf biliass.egg-info/
  rm -rf build/
  rm -rf dist/

ci-fmt-check:
  poetry run isort --check-only .
  poetry run black --check --diff .
  prettier --check '**/*.md'

ci-test:
  just gen-test-files
  poetry run pytest --reruns 3 --reruns-delay 1
  just clean

compile-protobuf:
  protoc --python_out=biliass protobuf/danmaku.proto

gen-test-files:
  poetry run python scripts/gen_test_files.py