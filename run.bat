@echo off

echo 🚀 Starting BIS RAG System...

<<<<<<< HEAD
=======

>>>>>>> ac73c94 (Update: pipeline, retriever improvements + config fixes)

echo 📦 Installing dependencies...
pip install -r requirements.txt

:: Create folders if missing
if not exist data mkdir data
if not exist data\processed mkdir data\processed

:: Build corpus if missing
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
