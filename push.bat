@echo off

echo 🚀 Pushing project to GitHub...

git status

git add .

git commit -m "Update: %date% %time%" || echo Nothing to commit

git pull origin main --rebase
git push origin main

echo ✅ Push complete!
pause