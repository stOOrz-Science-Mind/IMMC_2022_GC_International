@echo off
for /l %%i in (0, 1, 10000) do (
echo 我是log%%i.csv文件 >> log%%i.csv
)
echo 文件创建完毕
