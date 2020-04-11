import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://mark-joyce:FgKu3lwsX2ATDOcM@ms3cluster-ep3pg.mongodb.net/task_manager?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html', categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
    {
        'category_name': request.form.get('category_name'),
        'location_name': request.form.get('location_name'),
        'date_added': request.form.get('date_added'),
        'user_review': request.form.get('user_review'),
        'average_rent': request.form.get('average_rent'),
        'average_propertyprice': request.form.get('average_propertyprice'),
        'cgt_tax': request.form.get('cgt_tax'),
        'income_tax': request.form.get('income_tax'),
        'rental_tax': request.form.get('rental_tax'),
        'bestproperty_type': request.form.get('bestproperty_type'),
        'googlemaps_link': request.form.get('googlemaps_link'),
        'localproperty_link': request.form.get('localproperty_link'),
        'wikipage_link': request.form.get('wikipage_link')
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/task/<task_id>')
def task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    return render_template('tasklocation.html', task=the_task)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
