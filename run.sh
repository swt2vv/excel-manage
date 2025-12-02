docker build -t excel-flask-app:latest .
docker run -p 5000:5000 \
  --env AZURE_STORAGE_CONNECTION_STRING="CONNECTION_STRING_FROM_ENV" \
  excel-flask-app
 
 curl http://localhost:5000/api/v1/health