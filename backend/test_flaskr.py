import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'If the moon was made out of cheese would you eat it?',
            'answer': 'Yes',
            'category': 1,
            'difficulty': 1,
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test categories
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    # test questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])

    def test_get_paginated_questions_out_of_range(self):
        res = self.client().get('/questions?page=999999999')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(res.status_code, 404)

    # test questions by id
    def test_delete_question_that_exists(self):
        existingid = Question.query.first().id
        res = self.client().delete('/questions/' + str(existingid))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], existingid)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(
                Question.query.filter(Question.id == existingid).one_or_none(),
                None)

    def test_delete_question_that_does_not_exist(self):
        existingid = 999999
        res = self.client().delete('/questions/' + str(existingid))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test creating questions
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['created'])
        self.assertTrue(Question.query.filter(
            Question.id == data['created']).one_or_none())

    def test_fail_to_create_question(self):
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # test search questions
    def test_get_questions_by_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_get_no_questions_by_search(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'nmnmnmnmnmnmnmnmnnnm'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test questions by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_by_invalid_category(self):
        res = self.client().get('/categories/999999/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # test quiz
    def test_quiz_all(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [], 'quiz_category': {'type': 'All', 'id': 0}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_quiz_1(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'type': 'Science', 'id': 1}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_quiz_invalid_category(self):
        jsondata = {
            'previous_questions': [],
            'quiz_category': {'type': 'Trash', 'id': 99999999}
            }
        res = self.client().post('/quizzes', json=jsondata)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
