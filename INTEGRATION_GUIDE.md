# 🔗 Frontend-Backend Integration Guide

## Quick Start

### Option 1: Automatic Setup (Windows)

1. **Start Backend Server:**

   ```bash
   start_server.bat
   ```

   Wait for the message: `Uvicorn running on http://0.0.0.0:8000`

2. **Open Frontend:**

   ```bash
   start_frontend.bat
   ```

   Or simply open `index.html` in your browser

### Option 2: Manual Setup

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start Backend:**

   ```bash
   python app.py
   ```

3. **Open Frontend:**
   - Double-click `index.html` OR
   - Right-click → Open with → Chrome/Firefox

## ✅ Integration Features

### Backend (FastAPI)

- **Port:** 8000
- **CORS:** Enabled for all origins
- **Endpoints:**
  - `GET /` - Welcome message
  - `GET /health` - Health check
  - `POST /predict` - Image analysis

### Frontend (HTML/JavaScript)

- **Automatic Connection Check:** Tests backend availability on page load
- **Real-time Notifications:** Visual feedback for all actions
- **File Validation:**
  - Max size: 10MB
  - Formats: JPG, PNG, GIF, WebP, etc.
- **Loading States:** Shows progress during analysis
- **Error Handling:** Clear error messages for connection issues

## 🔍 Testing the Integration

### 1. Health Check

Open your browser console (F12) and check for:

```
✅ API connection successful
```

### 2. Upload Test

1. Click "Browse Files"
2. Select an image
3. Preview should appear in the right panel
4. Click "Analyze Now"
5. Results will appear in the left panel

### 3. API Documentation

Visit: `http://localhost:8000/docs`

- Interactive testing interface
- Try uploading images directly
- See request/response formats

## 🚨 Troubleshooting

### Error: "Backend server not running"

**Solution:**

```bash
python app.py
```

Make sure you see: `Uvicorn running on http://0.0.0.0:8000`

### Error: "Module not found"

**Solution:**

```bash
pip install -r requirements.txt
```

### Error: "Model not found"

**Solution:** Ensure these files are in the same directory:

- `flickr8k_model.keras`
- `tokenizer.pkl`

### CORS Error in Browser

**Solution:** The FastAPI app already has CORS enabled. If issues persist:

1. Check browser console for exact error
2. Verify API is running on port 8000
3. Try accessing `http://localhost:8000/health` directly

### Image Not Uploading

**Check:**

- File size < 10MB
- Valid image format (JPG, PNG, etc.)
- Backend server is running
- Browser console for errors

## 📡 API Request Example

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "image=@test_image.jpg"
```

### JavaScript (Frontend)

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(data.action, data.annotation);
```

### Python

```python
import requests

files = {'image': open('test.jpg', 'rb')}
response = requests.post('http://localhost:8000/predict', files=files)
print(response.json())
```

## 🌐 Deployment Options

### Local Network Access

Change in `app.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

Access from other devices: `http://YOUR_IP:8000`

### Public Internet (Ngrok)

```bash
pip install pyngrok
ngrok http 8000
```

Update frontend `API_URL` with the ngrok URL.

### Cloud Deployment

- **Azure:** Deploy with Azure App Service
- **AWS:** Use Elastic Beanstalk or EC2
- **Google Cloud:** Deploy to Cloud Run
- **Heroku:** Use Heroku CLI

## 📊 Performance Tips

1. **Model Loading:** Model is loaded once at startup (cached)
2. **Batch Processing:** For multiple images, implement queue system
3. **Image Optimization:** Frontend resizes images before upload (optional)
4. **Caching:** Add Redis for frequently analyzed images

## 🔐 Security (Production)

1. **Add Rate Limiting:**

   ```bash
   pip install slowapi
   ```

2. **API Key Authentication:**

   ```python
   from fastapi.security import APIKeyHeader
   ```

3. **File Size Limits:** Already implemented (10MB)

4. **CORS:** Update to specific origins:

   ```python
   allow_origins=["https://yourdomain.com"]
   ```

## ✨ Features in Action

- ✅ Automatic API health check on page load
- ✅ Image preview before upload
- ✅ Real-time loading indicators
- ✅ Toast notifications for all actions
- ✅ File validation (size & type)
- ✅ Graceful error handling
- ✅ Disabled button during processing
- ✅ Clear success/error messages

Your frontend and backend are now fully integrated! 🎉
