from flask import Flask, request, render_template_string
import requests
import os
from time import sleep
import time
import threading

app = Flask(__name__)
app.debug = True

# Constants
HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User   -Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'https://graph.facebook.com/'
}

stop_thread = threading.Event()

# Routes
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        message_prefix = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        stop_after = int(request.form.get('stopAfter'))
        stop_counter = 0

        def send_messages():
            nonlocal stop_counter
            if token_type == 'single':
                txt_file = request.files['txtFile']
                messages = txt_file.read().decode().splitlines()
                while not stop_thread.is_set():
                    try:
                        for message in messages:
                            api_url = f'https://graph.facebook.com/v13.0/me/messages?access_token={access_token}'
                            message = f"{message_prefix} {message}"
                            params = {'message': message, 'thread_id': thread_id}
                            response = requests.post(api_url, json=params, headers=HEADERS)
                            if response.status_code == 200:
                                print(f"Message sent using token {access_token}: {message}")
                                print(f"Conversation ID: {thread_id}")
                                stop_counter += 1
                                if stop_counter >= stop_after:
                                    stop_thread.set()
                            else:
                                print(f"Failed to send message using token {access_token}: {message}")
                            sleep(time_interval)
                    except Exception as e:
                        print(f"Error while sending message using token {access_token}: {message}")
                        print(e)
                        sleep(30)

            elif token_type == 'multi':
                token_file = request.files['tokenFile']
                tokens = token_file.read().decode().splitlines()
                txt_file = request.files['txtFile']
                messages = txt_file.read().decode().splitlines()
                while not stop_thread.is_set():
                    try:
                        for token in tokens:
                            for message in messages:
                                api_url = f'https://graph.facebook.com/v13.0/me/messages?access_token={token}'
                                message = f"{message_prefix} {message}"
                                params = {'message': message, 'thread_id': thread_id}
                                response = requests.post(api_url, json=params, headers=HEADERS)
                                if response.status_code == 200:
                                    print(f"Message sent using token {token}: {message}")
                                    print(f"Conversation ID: {thread_id}")
                                    stop_counter += 1
                                    if stop_counter >= stop_after:
                                        stop_thread.set()
                                else:
                                    print(f"Failed to send message using token {token}: {message}")
                                sleep(time_interval)
                    except Exception as e:
                        print(f"Error while sending message using token {token}: {message}")
                        print(e)
                        sleep(30)

        thread = threading.Thread(target=send_messages)
        thread.start()

        return render_template_string('''
        <!-- index.html -->
        <form action="/stop" method="post">
            <button type="submit">Stop</button>
        </form>
        ''')

@app.route('/stop', methods=['POST'])
def stop():
    stop_thread.set()
    return 'Stopped'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
