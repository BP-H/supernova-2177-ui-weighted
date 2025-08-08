from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your domain in production for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health():
    return {"status": "ok"}

# Example endpoint for your feed:
@app.get("/feed")
def feed():
    return [
        {
            "id": 1,
            "author_name": "Ann Guzman",
            "author_title": "PR Officer • 1st",
            "author_avatar": "https://api.dicebear.com/7.x/thumbs/svg?seed=ann",
            "text": "Prototype content — symbolic only.",
            "image_url": None,
            "stats": {"likes": 0, "comments": 0, "reposts": 0},
        }
    ]
