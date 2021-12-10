import time
import json

def fetch_lecture(hd_wid: str, session):
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/hdyy/yySave.do"
    data_json = {'HD_WID': hd_wid}
    form = {"paramJson": json.dumps(data_json)}
    result = session.post(url, data=form).json()
    if result['success'] is not False:
        print(result)
        return
    return result['code'], result['msg'], result['success']


def multi_threads(session, threads_id, hd_wid: str):
    i = 1
    while True:
        code, msg, success = fetch_lecture(hd_wid, session)
        print(f'线程{threads_id},第{i}次请求结果：{msg}；是否抢到:{success}')
        if success is True or msg == '当前活动预约人数已满，请重新选择' or msg == '已经预约过该活动，无需重新预约！':
            break
        else:
            i += 1
            time.sleep(1)
