import pandas as pd
from sqlalchemy import create_engine
import random
import datetime
import time
import random


def writeStuff():
    departments = {'计算机学院', '自动化学院', '信息学院', '计算研究院'}
    with open("data\\stuff.csv", "w", encoding='UTF-8') as f:
        f.write("SNo,Name,Department,Phone\n")
        s = "琦信厚束宛白兆飞昂姜从蓉柯思茵阎熙柔普景浩粘康适漆芳馨箕兰梦步芷若程寄蓝郑惜灵龙晓凡遇文耀抄秋莲养旻骞邝希蓉笃凝梦忻冰夏枚云臻苍涵易良亦玉高和颂介兴朝毓安春皋欣欣止荣轩犹庆生苗可心汝幼菱市思远藏春桃城碧螺嘉春冬尤清韵栋小宸次韶敏穆雨文帛云逸伊雨雪张天恩告鹏煊和夜天蒲康平刘平心"
        for i in range(40):
            name = s[i * 3: i * 3 + 3]
            department = departments.pop()
            departments.add(department)
            row = f"{i + 1},{name},{department},{str(random.randint(int(1e10), int(1.99e10)))}\n"
            print(row)
            f.write(row)


def writeEquipment():
    Manufactures = {'万斯得', '三思纵横', 'MTS', 'MTS', '济南新试金', '长春智能', '济南辰达', '万测', '济南锐玛', '济南联工'}
    departments = {'计算机学院', '自动化学院', '信息学院', '计算研究院'}
    with open("data\\Equipment.csv", "w", encoding='UTF-8') as f:
        with open("data\\buyIn.csv", "w", encoding='UTF-8') as f1:
            f.write("ENo,EName,Norm,Type,Manufacture,Status\n")
            f1.write("InNo,ENo,BDepart,SNoBuy,InMng,InDate,Fund,BConfirm\n")
            names = []
            with open("data\\1.txt", "r", encoding='UTF-8') as txt:
                rows = txt.readlines()
                names = [i.split(' ')[-1].replace('\n', '') for i in rows]
            print(names)
            namesS = set(names)
            alphabet = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"
            for i in range(300):
                manufacture = random.sample(Manufactures, 1)[0]
                name = random.sample(namesS, 1)[0]
                al = random.randint(3, 6)
                norm = "".join(random.sample(alphabet, al)) + '-' + str(random.randint(int(1e5), int(1.99e6)))
                t = "".join(random.sample(alphabet, random.randint(3, 5))) + '-' + str(random.randint(int(1e3), int(1.99e5)))
                row = f"{i + 1},{name},{norm},{t},{manufacture},{0}\n"
                print(row)
                f.write(row)
                d = random.sample(departments, 1)[0]
                fund = "".join(random.sample(alphabet, 3))
                row1 = f"{i + 1},{i + 1},{d},{random.randint(1,40)},{random.randint(41,45)},,{fund}基金,{random.randint(1,40)}\n"
                print(row1)
                f1.write(row1)


if __name__ == '__main__':
    # writeStuff()
    # # 初始化数据库连接，使用pymysql模块
    # # MySQL的用户：root, 密码:147369, 端口：3306,数据库：test
    engine = create_engine('mysql://root:112358@localhost/dbo?charset=utf8')
    # # 将新建的DataFrame储存为MySQL中的数据表，储存index列
    # df = pd.read_csv("data\\stuff.csv")
    # print(df)
    # df.to_sql('stuff', engine, index=False)
    # print('Read from and write to Mysql table successfully!')
    # writeEquipment()

    start_time = datetime.datetime.now()
    # 随机生成日期字符串
    for i in range(300):
        t = start_time + datetime.timedelta(weeks=random.randint(-100, 0))
        date = t.strftime("%Y-%m-%d")  # 将时间元组转成格式化字符串（2020-04-11 16:33:21）
        sql = f"UPDATE buyin SET InDate = '{date}' WHERE InNo = {i + 1}"
        engine.execute(sql)
        sql = f"UPDATE buyin SET ENo = {i + 1} WHERE InNo = {i + 1}"
        engine.execute(sql)
