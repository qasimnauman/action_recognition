# Action Recognition FastAPI Server

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 3. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### GET /

Health check - returns API status

### GET /health

Detailed health check including model status

### POST /predict

Upload image and get action prediction + caption

**Request:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your_image.jpg"
```

**Response:**

```json
{
  "status": "success",
  "action": "Running",
  "annotation": "A person running on the beach"
}
```

## 🔧 Configuration

### Update index.html

Change the API URL in your HTML file:

```javascript
const API_URL = "http://localhost:8000/predict";
```

### Enable Ngrok (Optional)

For public access:

```bash
pip install pyngrok
ngrok http 8000
```

Then update index.html with the ngrok URL.

## 📝 Python Client Example

```python
import requests

url = "http://localhost:8000/predict"
files = {'image': open('test_image.jpg', 'rb')}
response = requests.post(url, files=files)

result = response.json()
print(f"Action: {result['action']}")
print(f"Caption: {result['annotation']}")
```

## 🐳 Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t action-recognition-api .
docker run -p 8000:8000 action-recognition-api
```

## 🔐 Production Considerations

1. **CORS**: Update `allow_origins` in app.py to specific domains
2. **Authentication**: Add API key or JWT authentication
3. **Rate Limiting**: Implement rate limiting middleware
4. **File Size**: Add file size validation
5. **Logging**: Add proper logging for monitoring
6. **HTTPS**: Use reverse proxy (Nginx) with SSL certificate
