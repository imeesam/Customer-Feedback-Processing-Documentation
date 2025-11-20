from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import re
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

# Static files (for CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

keywords = ["good", "bad", "excellent", "poor"]

def process_feedback(file_content):
    lines = file_content.decode('utf-8').splitlines()
    total_feedback = len(lines)
    keyword_counts = {key: 0 for key in keywords}
    sentiment_score = 0

    for line in lines:
        line_lower = line.lower()
        for key in keywords:
            matches = re.findall(rf'\b{key}\b', line_lower)
            count = len(matches)
            keyword_counts[key] += count

        # sentiment score
        sentiment_score += line_lower.count('good') + line_lower.count('excellent')
        sentiment_score -= line_lower.count('bad') + line_lower.count('poor')

    most_common = max(keyword_counts, key=keyword_counts.get)
    return total_feedback, keyword_counts, sentiment_score, most_common

def generate_plot(keyword_counts):
    plt.figure(figsize=(6,4))
    plt.bar(keyword_counts.keys(), keyword_counts.values(), color='skyblue')
    plt.title("Keyword Frequency")
    plt.ylabel("Occurrences")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_base64

# ---------------------
# Routes
# ---------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    total, counts, sentiment, most_common = process_feedback(content)
    plot_base64 = generate_plot(counts)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total": total,
        "counts": counts,
        "sentiment": sentiment,
        "most_common": most_common,
        "plot_base64": plot_base64
    })
