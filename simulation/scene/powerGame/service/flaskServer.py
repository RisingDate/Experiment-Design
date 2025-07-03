import json

from flask import Flask, request
from flask_cors import CORS

from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent

app = Flask(__name__)
CORS(app)


@app.route('/requirementAnalysis', methods=['GET', 'POST'])
def requirementAnalysis():
    res = {
        'type': 'success',
        'msg': None,
        'data': {}
    }
    param = request.get_data().decode('utf8')
    param = json.loads(param)
    print(param['text'])
    ra = RequirementAnalysisAgent()
    parse_res = ra.requirement_analysis(param['text'])
    if type(parse_res) == str:
        res['type'] = 'error'
        res['msg'] = parse_res
    else:
        res['data'] = parse_res
        res['msg'] = '需求解析完成'
    return res


def run():
    print("Flask服务器启动成功，端口号为9090")
    app.run(host='localhost', port=9090, debug=True)


if __name__ == '__main__':
    # 启动服务
    run()
