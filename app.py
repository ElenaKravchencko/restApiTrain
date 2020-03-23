from flask import Flask, jsonify, abort, request, make_response
import requests

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': True
    }
]


@app.route('/todo/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if task_id not in [i['id'] for i in tasks]: #есть ли среди всех id  тот что мы передали
            abort(404) #ну если нет, то возвращаем ощибку
    else:
        task = list(filter(lambda t: t['id'] == task_id, tasks))[0] #иначе фильтруем все таски
        return jsonify({'task': task}) #и отдаем значение


# обработка ошибок
@app.errorhandler(404) #это декоратор куда передается код ошибки
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404) #любой словарь нужно возвращать в json файл
#чтобы можно было нормально обработать


# метод для получения всех задач
@app.route('/todo/api/v1/all_tasks', methods=['GET'])
def all_tasks():
    return jsonify(tasks)


@app.route('/todo/api/v1/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)

    tasks.append(request.json)
    return jsonify(request.json), 201



@app.route('/')
def index():
    res = requests.get('http://127.0.0.1:5000/todo/api/v1/tasks/1')
    print(res.status_code)
    print(res.json())

    ## несуществующий ключ
    res = requests.get('http://127.0.0.1:5000/todo/api/v1/tasks/3')
    print(res.status_code)
    print(res.json())

    ## все задачи
    print(requests.get('http://127.0.0.1:5000/todo/api/v1/all_tasks').json())

    ## добавить задачу
    js = {'key2': 'new_object2'}
    res=requests.post('http://127.0.0.1:5000/todo/api/v1/tasks', json=js)
    print(res.json())


    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)