ifndef SOURCE_FILES
	export SOURCE_FILES:=pandasetutils
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif
.PHONY: docs lint test format publish_test publish

format:
	# --preview指定する理由
	# ruffに合わせて、非ASCII文字の長さをunicode widthにするため
	# https://github.com/psf/black/pull/3445
	poetry run black ${SOURCE_FILES} ${TEST_FILES} --preview
	poetry run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero

lint:
	poetry run ruff ${SOURCE_FILES}
	# テストコードはチェックを緩和する
	# pygrep-hooks, flake8-datetimez, line-too-long, flake8-annotations, unused-noqa
	poetry run ruff check ${TEST_FILES} --ignore PGH,DTZ,E501,ANN,RUF100
	poetry run mypy ${SOURCE_FILES} ${TEST_FILES}
	# テストコードはチェックを緩和するためpylintは実行しない
	poetry run pylint --jobs=0 ${SOURCE_FILES}

test:
	# 並列実行してレポートも出力する
	poetry run pytest -n auto  --cov=kci --cov-report=html tests
