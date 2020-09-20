import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions][start:end]
    return questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resource={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = [category.format() for category in Category.query.all()]
        categories = {
                category['id']: category['type'] for category in categories
                }

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
            })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        questions = paginate_questions(request, questions)
        if len(questions) == 0:
            abort(404)
        categories = [category.format() for category in Category.query.all()]
        categories = {
                category['id']: category['type'] for category in categories
                }
        current_category = None

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories,
            'current_category': current_category
            })

    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted': q_id,
                'questions': questions,
                'total_questions': len(Question.query.all()),
                })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            data = request.get_json()
            print(data)

            new_question = data.get('question')
            new_answer = data.get('answer')
            new_category = data.get('category')
            new_difficulty = data.get('difficulty')
            question = Question(
                    question=new_question, answer=new_answer,
                    category=new_category, difficulty=new_difficulty
                    )
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': paginate_questions(request, Question.query.all()),
                'total_questions': len(Question.query.all())
                })

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json().get('searchTerm')
        query = Question.query.order_by(Question.id)
        query = query.filter(func.lower(Question.question)
                             .contains(func.lower(search_term))).all()
        if len(query) == 0:
            abort(404)

        questions = [question.format() for question in query]
        return jsonify({
            'success': True,
            'questions': questions,
            'current_category': None
            })

    @app.route('/categories/<int:c_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(c_id):
        try:
            category = Category.query.get(c_id)
            questions = Question.query.filter(Question.category == category.id)
            questions = questions.order_by(Question.id).all()
            paginated_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': c_id
                })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        c_id = body.get('quiz_category')['id']
        questions = []
        try:
            if c_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query
                questions = questions.filter(Question.category == c_id).all()
            if len(questions) == 0:
                abort(404)
            if len(body.get('previous_questions')) > 0:
                questions = [
                        question for question in questions
                        if question.id not in
                        body.get('previous_questions')
                        ]
            q = None
            if len(questions) > 0:
                q = random.choice(questions).format()

            return jsonify({
                'success': True,
                'question': q
                })
        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
            }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
            }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
            }), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
            }), 500

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
            }), 405

    return app
