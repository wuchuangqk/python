import json
import time

# 账号
account = {}
# 配置文件
bankFile = {}


def login():
    global bankFile
    global account
    print('请输入账号：')
    name = input()
    # 检查账号是否存在
    user = find_user(name)
    if not user:
        print('账号不存在')
        return False
    print('请输入密码：')
    password = input()
    if password != user['password']:
        print('密码错误')
        return False
    account = user
    print('登录成功')
    return True


def register():
    global bankFile
    print("请输入账户")
    name = input()
    user = find_user(name)
    if user:
        print('账户已存在')
    else:
        print("请输入密码")
        password = input()
        bankFile['account'].append({'name': name, 'password': password, 'money': 0})
        save_file()
        print('开户成功，余额：0')


def start():
    load_file()
    while True:
        print("1：登录 2：开户 3：退出")
        select = input()
        if select == '1':
            if login():
                menu()
        elif select == '2':
            register()
        elif select == '3':
            return


def menu():
    global account
    global bankFile
    while True:
        print("1：查看余额 2：存款 3：取款 4：转账 5：返回 6：查看存款记录 7：查看取款记录 8：查看转账记录")
        select = input()
        if select == '1':
            print('余额：%s' % account['money'])
        elif select == '2':
            print('请输入存款金额')
            num = int(input())
            if num < 0:
                print('金额不合法')
            else:
                account['money'] = account['money'] + num
                # 生成存款记录
                save_deposit_log(account['name'], num)
                save_file()
                print('存款成功，余额：%s' % account['money'])
        elif select == '3':
            print('请输入取款金额')
            num = int(input())
            if num < 0:
                print('金额不合法')
            elif num > account['money']:
                print('余额不足')
            else:
                account['money'] = account['money'] - num
                # 生成取款记录
                save_withdrawal_log(account['name'], num)
                save_file()
                print('取款成功，余额：%s' % account['money'])
        elif select == '4':
            print('请输入转账账户')
            name = input()
            target = find_user(name)
            if not target:
                print('转账账户不存在')
            elif target['name'] == account['name']:
                print('转账账户不能是自己')
            else:
                print('请输入转账金额')
                num = int(input())
                if num < 0:
                    print('金额不合法')
                elif num > account['money']:
                    print('余额不足')
                else:
                    account['money'] = account['money'] - num
                    target['money'] = target['money'] + num
                    # 生成转账记录
                    save_transfer_log(account['name'], target['name'], num)
                    save_file()
                    print('转账成功，余额：%s' % account['money'])
        elif select == '5':
            return
        elif select == '6':
            user_logs = find_user(account['name'], 'deposit_log')
            print('账户       存款时间        存款金额')
            if len(user_logs['logs']) == 0:
                print('没有查询到存款记录')
            for log in user_logs['logs']:
                print('[%s]     [%s]    [%s元]' % (account['name'], log['time'], log['money']))
        elif select == '7':
            user_logs = find_user(account['name'], 'withdrawal_log')
            print('账户       取款时间        取款金额')
            if len(user_logs['logs']) == 0:
                print('没有查询到取款记录')
            for log in user_logs['logs']:
                print('[%s]     [%s]    [%s元]' % (account['name'], log['time'], log['money']))
        elif select == '8':
            user_logs = find_user(account['name'], 'transfer_log')
            print('转账账户        转账时间        转账金额')
            if len(user_logs['logs']) == 0:
                print('没有查询到转账记录')
            for log in user_logs['logs']:
                print('[%s]     [%s]    [%s元]' % (log['target'], log['time'], log['money']))


def load_file():
    """
    读取文件
    :return:
    """
    with open('account.json', 'r') as f:
        global bankFile
        bankFile = json.load(f)
        count = len(bankFile['account'])
        print('系统共有%s个用户' % count)


def save_file():
    """
    写入文件
    :return:
    """
    with open('account.json', 'w') as w:
        json.dump(bankFile, w)


def find_user(name, list='account'):
    """
    通过账户名称查找用户
    :param list:
    :param name:
    :return:
    """
    global bankFile
    for user in bankFile[list]:
        if user['name'] == name:
            return user


def save_deposit_log(name, money):
    """
    添加存款记录
    :param name:账户
    :param money: 存款金额
    :return:
    """
    global bankFile
    # 日期，金额
    log = {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'money': money}
    user = find_user(name, 'deposit_log')
    if not user:
        bankFile['deposit_log'].append({'name': name, 'logs': [log]})
    else:
        user['logs'].append(log)


def save_withdrawal_log(name, money):
    """
    添加取款记录
    :param name:账户
    :param money: 取款金额
    :return:
    """
    global bankFile
    # 日期，金额
    log = {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'money': money}
    user = find_user(name, 'withdrawal_log')
    if not user:
        bankFile['withdrawal_log'].append({'name': name, 'logs': [log]})
    else:
        user['logs'].append(log)


def save_transfer_log(name, target_name, money):
    """
    添加转账记录
    :param target_name: 转账账户
    :param name:账户
    :param money: 转账金额
    :return:
    """
    global bankFile
    # 日期，金额
    log = {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'money': money, 'target': target_name}
    user = find_user(name, 'transfer_log')
    if not user:
        bankFile['transfer_log'].append({'name': name, 'logs': [log]})
    else:
        user['logs'].append(log)


start()
