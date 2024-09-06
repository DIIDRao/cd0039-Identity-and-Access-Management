import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
# from auth import AuthError

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@requires_auth('get:drinks')
@app.route("/drinks")
def get_drinks():
        drinks = Drink.query.all()
        print(drinks)
        formatted_drinks = [drink.short() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": formatted_drinks
        })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail():
        drinks = Drink.query.all()
        print(drinks)
        formatted_drinks = [drink.long() for drink in drinks]
        # print(formatted_drinks)
        return jsonify({
            "success": True,
            "drinks": formatted_drinks
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks():
        data = request.get_json(force=True)
        drink = Drink(
                    title=data.get('title'),
                    recipe=data.get('recipe')
                )
        drink = Drink.insert(drink)
        formatted_drinks = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(id):
   # Retrieve data from the request
   data = request.get_json(force=True)
   # Update Drink in the  database
   drink = Drink.query.get_or_404(id)
   print('found')
   print(drink)
   drink.title = data.get('title')
   drink.update()
   # Return success message
   formatted_drinks = [drink.long()]
   return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
   drink = Drink.query.get_or_404(id)
   print('found')
   print(drink)
   drink.delete()
   # Return success message
   return jsonify({
            'success': True,
            'delete': id
        })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error): 
  return jsonify({ 
    "success": False, 
    "error": 404, 
    "message": "resource not found" 
  }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
