# Case Machine Learning Engineer - Airpoirts delay
## About 🔎
This is an API wich you can preview a flight delay using a Machine Learn model.

### Implemented features ✅
- [x] Notebook with questions answeared with pyspark, model and the final question related to enrich the database
- [x] Model .pkl file
- [x] API health endpoint
- [x] Load model endpoint
- [x] User the model to make a prediction endpoint
- [x] Show model prediction history endpoint
- [x] Add tests related to each endpoint
- [x] Refactor the code
### Future improvements 🔮
- [ ] Add more tests
- [ ] Improve model metrics

## 📍 API Endpoints</h2>

​
| route               | description                                          
|----------------------|-----------------------------------------------------
| <kbd>POST /model/predict/</kbd>     | Receives a payload with flight information and returns the estimated delay at the destination
| <kbd>POST /model/load/</kbd>     | Receives the model and leave the API ready to make predictions
| <kbd>GET /model/history/</kbd>     | Displays the history of predictions made (the input payload + the predicted outputs)
| <kbd>GET /health/</kbd>     | Returns the health of the API
## Technologies
The following tools and frameworks were used in the construction of the project:<br>

  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

## How to run
1. Clone this repository
2. Navigate to the project directory
```bash
cd case-airports
```
3. Build the Docker image
```bash
docker compose build
docker compose up
```
5. Access the API
```bash
http://localhost:8000/
```
