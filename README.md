# videoanalyzer-fastapi

To run this project 
```bash
uvicorn main:app --reload
```

Use curl or postman to validate the response 
```bash
curl -X 'POST' \
   'http://127.0.0.1:8000/analyze-video/' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
   "gcs_uri": "gs://your-bucket/path/to/your_video.mp4",
   "analysis_type": "description"
 }
```
