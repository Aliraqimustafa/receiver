from pyngrok import ngrok
from flask import Flask, request, jsonify
import importlib

def get_func(module_name , func_name):
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func

def kill(kill_input):
    if kill_input:
         [ngrok.disconnect(url.public_url) for url in ngrok.get_tunnels()]
        # print('Disconnection completed')

def final_func(module_or_code):
    if module_or_code == 'mod':
        module_name = input('Enter module name : ')
        func_name = input('Enter function naem : ')
    else:
        module_name = '__main__'
        func_name = input('Enter function naem : ')
    func = get_func(module_name , func_name)
    return func

def create_app(app_type = 'non-json'):
    app = Flask(__name__)

    module_or_code = input('You have module or code ? ')
    
    func = final_func(module_or_code)
    kill_input = input('Kill ? ')
    port = input('Enter PORT : ')
    subdomain = input('Enter subdomain : ')
    kill(kill_input)
    __PORT__ = 5000 if port == '' else int(port)
    public_url = ngrok.connect(__PORT__).public_url
    print(f'\n\n\n Now you can send post request : {public_url}\n\n\n')
    @app.route(f'/{subdomain}', methods=['POST'])
    def receive_data():
        try:
            data = request.get_json()
        except:
            # data = request.get_data(as_text=True)
            data = request.data
        result  = func(data)
        if app_type == 'json':
            response = {"result": result}
            response = jsonify(response), 200
        else:
            response = result , 200
        return response
    app.run(debug=False, port=__PORT__)


if __name__ == '__main__':
    create_app()

