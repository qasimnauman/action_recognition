import io
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize FastAPI app
app = FastAPI(
    title="Action Recognition API",
    description="AI-powered image action detection and caption generation",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and tokenizer
MODEL_PATH = 'flickr8k_model.keras'
TOKENIZER_PATH = 'tokenizer.pkl'

print("⏳ Loading Model & Tokenizer...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, 'rb') as f:
        tokenizer = pickle.load(f)
    
    # Get max_length from tokenizer
    max_length = max(len(seq) for seq in tokenizer.texts_to_sequences(tokenizer.word_index.keys()))
    print(f"✅ Model loaded successfully! Max length: {max_length}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    tokenizer = None
    max_length = 34  # Default fallback

def generate_caption(img_array):
    """Generate caption from image array"""
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length, padding='post')

        yhat = model.predict([img_array, sequence], verbose=0)
        yhat = np.argmax(yhat)

        word = tokenizer.index_word.get(yhat)

        if word is None or word == 'endseq':
            break

        # Prevent repetition
        if word in in_text.split()[-2:]:
            break

        in_text += ' ' + word

    return in_text.replace('startseq', '').strip()

def detect_action(caption: str) -> str:
    """Detect action from generated caption"""
    caption_lower = caption.lower()
    
    # Priority 1: Explicit actions
    if any(w in caption_lower for w in ["run", "running", "sprinting", "jogging"]):
        return "Running"
    elif any(w in caption_lower for w in ["jump", "jumping", "leap", "leaping", "fly", "midair"]):
        return "Jumping"
    elif any(w in caption_lower for w in ["swim", "swimming", "diving"]):
        return "Swimming"
    elif any(w in caption_lower for w in ["ride", "riding", "bike", "bicycle", "motorcycle"]):
        return "Cycling/Riding"
    
    # Priority 2: Environment-based inference
    elif any(w in caption_lower for w in ["water", "pool", "ocean", "river", "lake", "beach"]):
        return "Swimming"
    elif any(w in caption_lower for w in ["grass", "field", "park", "track"]):
        return "Running"
    elif any(w in caption_lower for w in ["mountain", "rock", "climb"]):
        return "Climbing"
    
    else:
        return "General Pose"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "message": "Action Recognition API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None
    }

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    Predict action and generate caption from uploaded image
    
    Args:
        image: Image file (JPG, PNG, etc.)
    
    Returns:
        JSON response with detected action and generated annotation
    """
    # Validate model is loaded
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert('RGB').resize((224, 224))
        
        # Preprocess
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Generate caption
        caption = generate_caption(img_array)
        
        # Detect action
        action = detect_action(caption)
        
        return JSONResponse({
            "status": "success",
            "action": action,
            "annotation": caption.capitalize()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
