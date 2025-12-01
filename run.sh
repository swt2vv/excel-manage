docker build -t excel-flask-app .
docker run -p 5000:5000 \
  --env AZURE_STORAGE_CONNECTION_STRING="AZURE_STORAGE_CONNECTION_STRING" \
  excel-flask-app
 