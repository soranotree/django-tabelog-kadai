#!/bin/bash

# isortチェック : モジュールインポート順チェック
echo -e "\e[36misortチェック開始\e[m"
isort --check .

if [ $? -ne 0 ]; then
    echo -e "\e[31misortチェックNG\e[m"
    exit 1
fi
echo ""

# blackチェック : コード書式チェック
echo -e "\e[36mblackチェック開始\e[m"
black --check .

if [ $? -ne 0 ]; then
    echo -e "\e[31mblackチェックNG\e[m"
    exit 1
fi
echo ""

# mypyチェック : 型ヒントチェック
echo -e "\e[36mmypyチェック開始\e[m"
mypy . --check-untyped-defs

if [ $? -ne 0 ]; then
    echo -e "\e[31mmypyチェックNG\e[m"
    exit 1
fi
echo ""

# flake8チェック : 構文解析チェック
echo -e "\e[36mflake8チェック開始\e[m"
flake8 .

if [ $? -ne 0 ]; then
    echo -e "\e[31mflake8チェックNG\e[m"
    exit 1
fi

# 単体テスト
echo -e "\e[36m単体テスト開始\e[m"
pytest ./tests/

if [ $? -ne 0 ]; then
    echo -e "\e[31m単体テストNG\e[m"
    exit 1
fi

echo "全チェック合格"
exit 0
