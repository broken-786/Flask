from flask import Flask, request, render_template_string
import requests
import os
from time import sleep
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        if token_type == 'single':
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode().splitlines()

            while True:
                try:
                    for message1 in messages:
                        api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                        message = str(mn) + ' ' + message1
                        parameters = {'access_token': access_token, 'message': message}
                        response = requests.post(api_url, data=parameters, headers=headers)
                        if response.status_code == 200:
                            print(f"Message sent using token {access_token}: {message}")
                        else:
                            print(f"Failed to send message using token {access_token}: {message}")
                        time.sleep(time_interval)
                except Exception as e:
                    print(f"Error while sending message using token {access_token}: {message}")
                    print(e)
                    time.sleep(30)

        elif token_type == 'multi':
            token_file = request.files['tokenFile']
            tokens = token_file.read().decode().splitlines()
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode().splitlines()

            while True:
                try:
                    for token in tokens:
                        for message1 in messages:
                            api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                            message = str(mn) + ' ' + message1
                            parameters = {'access_token': token, 'message': message}
                            response = requests.post(api_url, data=parameters, headers=headers)
                            if response.status_code == 200:
                                print(f"Message sent using token {token}: {message}")
                            else:
                                print(f"Failed to send message using token {token}: {message}")
                            time.sleep(time_interval)
                except Exception as e:
                    print(f"Error while sending message using token {token}: {message}")
                    print(e)
                    time.sleep(30)

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ɕ๏ƞvo səɽvəɽ</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    
  label{
    color: white;
}

.file{
    height: 30px;
}
body{
    background-image: url('https://i.ibb.co/9bDrvxs/ee6ad5f22fd0ab1086a3643ddc018cb1.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    color: white;

}
    .container{
      max-width: 350px;
      height: 600px;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      box-shadow: 0 0 15px white;
            border: none;
            resize: none;
    }
        .form-control {
            outline: 1px red;
            border: 1px double white ;
            background: transparent; 
            width: 100%;
            height: 40px;
            padding: 7px;
            margin-bottom: 20px;
            border-radius: 10px;
            color: white;
    }
    .header{
      text-align: center;
      padding-bottom: 20px;
    }
    .btn-submit{
      width: 100%;
      margin-top: 10px;
    }
    .footer{
      text-align: center;
      margin-top: 20px;
      color: #888;
    }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
    }
    .whatsapp-link i {
      margin-right: 5px;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mb-3"> ๏ ᴏꜰꜰʟɪɴᴇ ᴄᴏɴᴠᴏ ꜱᴇʀᴠᴇʀ ๏
    <h1 class="mt-3">◉𝐛ɽ๏ʞəƞ fɣʈəɽ◉</h1>
  </header>

  <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenType">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴅᴀɪ ᴋᴇ ʟɪʏᴇ ᴛᴏᴋᴇɴ ᴛʏᴩ:</label>
        <select class="form-control" id="tokenType" name="tokenType" required>
          <option value="single">ᴀᴠɴɪ ʀᴀɴᴅɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ꜱɪɴɢʟᴇ ᴛᴏᴋᴇɴ</option>
          <option value="multi">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ᴍᴜʟᴛɪ ᴛᴏᴋᴇɴ</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="accessToken">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ᴛᴏᴋᴇɴ ᴅᴀʟ:</label>
        <input type="text" class="form-control" id="accessToken" name="accessToken">
      </div>
      <div class="mb-3">
        <label for="threadId">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴋᴀ ʟɪɴᴋ ᴅᴀʟ:</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ʜᴀᴛᴇʀꜱɴᴀᴍᴇ ᴅᴀʟ:</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ɴᴩ ꜰɪʟᴇ ᴅᴀʟ:</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3" id="multiTokenFile" style="display: none;">
        <label for="tokenFile">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴛ ᴍᴇ (ᴍᴜʟᴛɪ ᴛᴏᴋᴇɴ ᴅᴀʟ ):</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
      </div>
      <div class="mb-3">
        <label for="time">ᴀᴠɴɪ ᴋᴏ ᴄʜᴏᴅɴᴇ ᴋɪ ꜱᴩᴇᴇᴅ:</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">ᴀᴠɴɪ ᴋɪ ᴄʜᴜᴅᴀɪ ᴏɴ ᴋʀ</button>
    </form>
  </div>
  <footer class="footer">
    <p>ꜱᴇʀᴠᴇʀ ᴋᴏ ᴀᴠɴɪ ʀᴀɴᴅɪ ᴋɪ ᴄʜᴜᴛ ᴍᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ ʙɴᴀʏᴀ ʜᴀɪ</p>
    <p>ᴀᴠɴɪ ᴄʜᴜᴅᴀɪ ᴛᴏᴏʟ</p>
    
  </footer>

  <script>
    document.getElementById('tokenType').addEventListener('change', function() {
      var tokenType = this.value;
      document.getElementById('multiTokenFile').style.display = tokenType === 'multi' ? 'block' : 'none';
      document.getElementById('accessToken').style.display = tokenType === 'multi' ? 'none' : 'block';
    });
  </script>
</body>
</html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
