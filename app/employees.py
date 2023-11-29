from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql

employees = Blueprint('employees', __name__, template_folder='app/templates')

@employees.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=data)

@employees.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        phone = request.form['phone']
        carrer = request.form['carrer']
        country = request.form['country']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO employees (name, lastname, phone, carrer, country) VALUES (%s,%s,%s,%s,%s)",
                (name, lastname, phone, carrer, country))
            mysql.connection.commit()
            flash('Employee Added successfully')
            return redirect(url_for('employees.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('employees.Index'))

@employees.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-employee.html', employee=data[0])

@employees.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        phone = request.form['phone']
        carrer = request.form['carrer']
        country = request.form['country']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE employees
            SET name = %s,
                lastname = %s,
                phone = %s,
                carrer = %s,
                country = %s
            WHERE id = %s
        """, (name, lastname, phone, carrer, country, id))
        flash('Employee Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('employees.Index'))

@employees.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM employees WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('employees.Index'))
