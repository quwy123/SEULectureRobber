import sys
import time

def get_lecture_list(session):
    '''获取课程列表'''
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/*default/index.do#/hdyy"

    session.get(url)
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/modules/hdyy/hdxxxs.do"
    form = {"pageSize": 12, "pageNumber": 1}
    response = session.post(url, data=form).json()
    rows = response['datas']['hdxxxs']['rows']
    return rows


def get_lecture_info(w_id, session):
    '''获取讲座信息'''
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/modules/hdyy/hdxxxq_cx.do"
    data_json = {'WID': w_id}
    res = session.post(url, data=data_json)
    try:
        result = res.json()['datas']['hdxxxq_cx']['rows'][0]
        return result
    except Exception:
        print("课程信息获取失败")
        return False

def print_lecture(session):
    lecture_list = get_lecture_list(session)  #获取讲座列表
    print("----------------讲座列表----------------")
    for lecture in lecture_list:
        print("讲座wid：", end=" ")
        print(lecture['WID'], end="  |")
        print("讲座名称：", end=" ")
        print(lecture['JZMC'])
        # print("预约开始时间：", end=" ")
        # print(lecture['YYKSSJ'], end="  |")
        # print("预约结束时间：", end=" ")
        # print(lecture['YYJSSJ'], end="  |")
        # print("活动时间：", end=" ")
        # print(lecture['JZSJ'])
    print("----------------讲座列表end----------------")

def set_figure(session):
    lecture_info = False
    while True:
        print("\n请输入讲座wid")
        wid = input()
        lecture_info = get_lecture_info(wid, session)
        if lecture_info is not False:
            try:
                lecture_name = lecture_info['JZMC']
            except Exception:
                print("讲座信息获取失败")
                continue

            print(f"确认讲座名称：{lecture_name}\n\n==========确认请按y，重新选择请按n==========")
            confirm = input()
            if confirm == 'y' or confirm == 'Y':
                break
            else:
                pass

    print("本程序将会提前10秒开抢，请保证网络通畅\n")
    advance_time = 10
    current_time = int(time.time())
    begin_time = int(time.mktime(time.strptime(lecture_info['YYKSSJ'], "%Y-%m-%d %H:%M:%S")))
    end_time = int(time.mktime(time.strptime(lecture_info['YYJSSJ'], "%Y-%m-%d %H:%M:%S")))
    if current_time > end_time:
        print("预约时间已结束")
        sys.exit(0)
    while current_time < begin_time - advance_time:
        current_time = int(time.time())
        print(f'等待{begin_time - advance_time - current_time}秒, 点右上角×号将退出抢讲座')
        time.sleep(1)
    return wid
