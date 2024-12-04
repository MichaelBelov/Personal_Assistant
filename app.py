from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)
tasks = {
  'tasks': [
    {
      'id': 1,
      'title': 'Repair Porsche',
      'description': 'Отвезти машину в сервис',
      'done': 'false'
    },
    {
      'id': 2,
      'title': 'Meeting with Vox',
      'description': 'Место: киностудия Ви',
      'done': 'true'
    },
{
      'id': 3,
      'title': 'Слетать в отпуск',
      'description': 'Купить билеты (не забыть апгрейд до бизнеса)',
      'done': 'false'
    },
{
      'id': 4,
      'title': 'Акции',
      'description': 'Продать Роснефть',
      'done': 'false'
    },
  ]
}



@app.route('/')
def main():
    return 'Bonjour!'

@app.route('/tasks', methods=['GET'])
def tasks_web():
    done_params = request.args.get('done')
    query_params = request.args.get('query')
    page_params = request.args.get('page')
    per_page_params = request.args.get('per_page')
    filtered_tasks = {'tasks': []}
    ans = {'tasks': []}
    try:
        if done_params:
            done_params = done_params.lower()
            for i in tasks['tasks']:
                if i['done'] == done_params:
                    filtered_tasks['tasks'].append(i)
        else:
            filtered_tasks['tasks'] = tasks['tasks']
        if query_params:
            query_params = query_params.lower()
            for i in filtered_tasks['tasks']:
                if query_params in i['description'] + i['title']:
                    ans['tasks'].append(i)
        else:
            ans = filtered_tasks
    except Exception as e:
        return str(e)
    if page_params and per_page_params:
        page = int(page_params)
        per_page = int(per_page_params)
        start = (page - 1) * per_page
        end = page * per_page
        if end > len(ans['tasks']):
            end = len(ans['tasks'])
        if len(ans['tasks'][start:end]) == 0:
            abort(404)
        return jsonify({'tasks': ans['tasks'][start:end], 'page': page, 'per_page': per_page, 'total': len(ans['tasks'])})
    else:
        return jsonify(ans)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def tasks_web_id(task_id):
    for j in tasks['tasks']:
        if j['id'] == task_id:
            return jsonify(j)
    abort(404)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if 'title' in data:
        if 'description' not in data:
            data['description'] = ''
        tasks['tasks'].append({'id': len(tasks['tasks']) + 1, 'title': data['title'], 'description': data['description'], 'done': 'false'})
        return jsonify(tasks['tasks'][-1]), 201
    else:
        abort(400)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    answer = ''
    if 'done' in data and 'title' in data and 'description' in data:
        for j in range(len(tasks['tasks'])):
            if tasks['tasks'][j]['id'] == task_id:
                tasks['tasks'][j] = {'id': task_id, 'title': data['title'], 'description': data['description'], 'done': data['done']}
                ans = tasks['tasks'][j]
        if answer != '':
            return answer
        else:
            abort(404)
    else:
        abort(400)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not(0 < task_id < len(tasks['tasks']) + 1):
        print(len(tasks['tasks']))
        abort(404)
    elif task_id == len(tasks['tasks']):
        tasks['tasks'].pop(task_id - 1)
    else:
        for i in range(task_id, len(tasks['tasks'])):
            tasks['tasks'][i]['id'] -= 1
        tasks['tasks'].pop(task_id - 1)
    return jsonify({'result': 'Задача успешно удалена'})

if __name__ == '__main__':
    app.run(debug=True)