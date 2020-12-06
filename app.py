from flask import Flask
from flask import render_template
from flask import request

import base

app = Flask(__name__)


# 获取数据
def get_data(cookie):
    co = base.Core(cookie)
    return co.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    # cookie
    cookie = request.args.get('cookie')
    # 工时
    times = 0

    if cookie is not None:
        try:
            times = get_data(cookie)
        except Exception as e:
            times = -1
            print(e)
    return render_template('index.html', num=times)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

