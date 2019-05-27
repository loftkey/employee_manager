# -*- coding: utf-8 -*-
"""
Python naming style 
https://google.github.io/styleguide/pyguide.html#Naming

Flask Json support 
http://flask.pocoo.org/docs/1.0/api/#module-flask.json
"""

from flask import Flask, json, jsonify, request
from emp import Employee

a, b, c = Employee('Andy', '001', 'CSE', 'Professor'), \
            Employee('Beth', '002', 'CSE', 'Student'), \
            Employee('Chris', '003', 'CSE', 'Student')

employees = {a.get_id_number():a, b.get_id_number():b, c.get_id_number():c}

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'


@app.route('/employee/<eid>', methods = ['GET', 'DELETE', 'PUT'])
def api_get_info(eid):
    '''
    try updating a raw JASON in PUT
    {"name":"X", "title":"XXX"}
    '''
    if request.method == 'DELETE':
        del employees[eid]
        return eid+ ' is deleted'

    elif request.method == 'PUT':
        if eid not in employees.keys():
            return eid + ' Not Found'
        data = request.get_json(force=True)
        t = employees[eid]
        t.set_name(data['name'])
        t.set_title(data['title'])
        t.set_department(data['department'])
        return eid+ ' updated'
    
    else:
        empy = employees[eid]
        return jsonify(name = empy.get_name(), title = empy.get_title(), department = empy.get_department())

@app.route('/employee', methods = ['GET','POST'])
def api_list_and_insert():
    '''
    try adding a raw JASON in the POST request body
    {"name":"C", "id":"004", "department":"CSE", "title":"Staff"}
    '''
    if request.method == 'POST': # add employee
        data = request.get_json(force=True)
        name = data['name']
        eid = data['id']
        dept = data['department']
        title = data['title']
        employees[eid] = Employee(name,eid,dept,title)
        return str(employees[eid])
    else: # list all employees
        return jsonify({key:str(val) for key, val in employees.items()})


if __name__ == '__main__':
    app.run(debug=False, port = 5000)

