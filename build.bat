@echo off
echo Generate requirements.txt
python -m pipreqs.pipreqs .

echo Build docker
docker build -t meldianov_test_service .