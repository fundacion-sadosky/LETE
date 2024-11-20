call %1
cd %2
python -m rasa run --enable-api --cors "*" -p 5012
exit