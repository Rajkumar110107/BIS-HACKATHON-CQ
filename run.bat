@echo off

echo 🚀 Starting BIS RAG System...

python -V >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python (>=3.9)
    pause
    exit /b
)

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