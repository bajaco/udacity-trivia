# Full Stack Trivia API Backend

## API Documentation
### Getting Started
- Base URL: This application is run locally. The default URL for the backend is ```http://localhost:5000/```.
- This application does not require authentication.
### Error Handling
- Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}
```
Errors are implented for the following standard http response codes:
- 404: resource not found
- 422: unprocessable
- 400: bad request
- 500: internal server error
- 405: method not allowed
### Endpoints
##### GET /categories
Get all categories.
##### GET /questions
Get all questions.
##### DELETE /questions/id
Delete a question by id.
##### POST /questions
Add a question.
##### POST /questions/search
Search questions.
##### GET /categories/id/questions
Get questions by category id.
##### POST /quizzes
Get random question for quiz.

### GET /categories
- No arguments required.
- Returns object with single key/value pair, 'categories': and an object containing key/value pairs for id number and string category.
- Example:
```
$ curl localhost:5000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
### GET /questions
- No arguments required.
- Returns object with 'categories' key corresponding to categories object, 'current_category', 'questions' corresponding to questions object, 'success', and 'total_questions'.
- Example:
```
$ curl localhost:5000/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, ...
  ],
  "success": true, 
  "total_questions": 20
}
```
### DELETE /questions/id
- Requires id argument.
- Returns object containing 'deleted' corresponding to deleted id, 'questions' corresponding to questions object, 'success', and 'total_questions'
- Example:
```
$ curl -X DELETE localhost:5000/questions/5
{
  "deleted": 5, 
  "questions": [
    ...
  ], 
  "success": true, 
  "total_questions": 16
}
```
### POST /questions
- Requires JSON object containing 'question', 'answer', 'category' and 'difficulty' arguments.
- Returns object containing 'success', 'created' corresponding to id of created question, 'questions' corresponding to questions object and 'total_questions'.
- Example:
```
$ curl -X POST -H "Content-Type: application/json" -d '{"question": "New Question", "answer": "New Answer", "category": 1, "difficulty": 1}' localhost:5000/questions
{
  "created": 25, 
  "questions": [
    ...  
  ], 
  "success": true, 
  "total_questions": 16

```
### POST /questions/search
- Requires JSON object containing 'searchTerm'
- Returns object containing 'success', 'questions' corresponding to questions object of relevant results and 'current_category'
- Example:
```
$ curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "africa"}' localhost:5000/questions/search
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true
}

```
### GET /categories/id/questions
- Requires id argument
- Returns object containing 'success', 'questions' corresponding to questions object containing relevant questions, 'total_questions', and 'current_category'.
- Example:
```
$ curl -X GET localhost:5000/categories/2/questions
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, ... 
  ], 
  "success": true, 
  "total_questions": 4
}

```
### POST /quizzes
- Requires JSON object containing 'previous_questions' array, and 'quiz_category' object containing 'id' and 'type'.
- Returns object containing 'success' and 'question' corresponding to randomly chosen question.
- Example:
```
$ curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[24,25],"quiz_category":{"type":"Science","id":"1"}}' localhost:5000/quizzes
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
