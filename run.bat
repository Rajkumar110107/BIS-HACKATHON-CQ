@echo off

echo 🚀 Starting BIS RAG System...

echo 📦 Installing dependencies...
pip install -r requirements.txt

if not exist data\processed\corpus.json (
    echo 📚 Building corpus...
    python src\ingest.py
) else (
    echo ✅ Corpus already exists, skipping...
)

echo ⚡ Running inference...
python inference.py --input sample.json --output result.json

echo 📄 Result:
type result.json

echo ✅ Done!
pause