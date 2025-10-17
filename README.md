# e-commerce-app
E-commerce app with angular, python fastAPI, and kafka

To run frontend:
Navigate to frontend folder and run ```ng serve```

To run backend:
Activate venv and then run 
```pip install -r requirements.txt```
```python -m app.seed_data```
```uvicorn app.main:app --reload```

To run kafka:
run docker-compose up -d
