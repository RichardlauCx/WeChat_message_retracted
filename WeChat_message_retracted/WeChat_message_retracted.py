# By Richard
import itchat
import re
import pyttsx3  # 文字转语音库

# def main():
#     pass  # 占位符
# if __name__ == '__main__':  # 内建变量
#     main()  # 调用函数
# 把所有的消息记录(保存）下来，一旦有撤回就把消息找出来 《---主旨
data_dict = dict()  # 定义一个字典全局变量


@itchat.msg_register(['Text', 'Picture', 'Recording', 'Video'])  # 自动调用下方函数机制,增加语音、图片和视频信息的接收
def message(msg):  # 保存信息
    print(msg)
    global data_dict  # 改写字典全局变量
    name = itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 找到用户昵称（提取出来）
    print(name)  # 输出用户昵称信息
    id = msg['MsgId']   # 消息的内容是什么，以及是谁发的？ 并且id对应信息是唯一的
    type = msg['Type']
    if type == 'Text':
        text = msg['Text'].strip()  # 提取出文本类消息，去掉左右空格
        content = text
    else:  # 除文本以外的信息
        msg['Text'](msg['FileName'])  # itchat的附件下载方法，储存在msg的Text键中
        content = msg['FileName']  # 获取文件名
    data_dict[id] = {'name': name, 'content': content, 'type': type}  # 信息内容封装


@itchat.msg_register('Note')  # 消息注册机制，接收到的微信通知，自动调用下方函数
def notice(msg):
    print(msg)
    if '撤回了一条消息' in msg['Text'] or '已回收一則訊息' in msg['Text'] or 'recalled a message' in msg['Text']:  # 简体中文、繁体中文和英文   ！！！！！！！
        try:
            # old_msg_id = re.search('(\<msgid\>(.*?)\<\/msgid\>)', msg['Content']).group(1)  # 错误示范
            old_msg_id = re.search('\<msgid\>(.*?)\<\/msgid\>', msg['Content']).group(1)  # 正则表达式所提取第二项的内容，问号表示为贪婪符
            # old_msg_id = re.search('((\<msgid\>)(.*?)(\<\/msgid\>))', msg['Content']).group(3)
            # old_msg_id = re.search(r'^hello\s(.*)\sfine',b).group()
            # print(old_msg_id)
            # print('data_dict: {}'.format(data_dict))
            name = data_dict[old_msg_id]['name']  # 找出昵称
            content = data_dict[old_msg_id]['content']  # 找出内容
            type = data_dict[old_msg_id]['type']  # 做判断找出类型
            toUserName = itchat.search_friends(nickName=name)[0]['UserName']
            if type == 'Text':
                tip = name + '撤回了一条消息，撤回的内容为：' + content  # 拼接信息
                itchat.send(tip, 'filehelper')  # 发信息给文件助手
                # itchat.send(tip, toUserName)  # 发送给撤回对象
            else:
                tip = name + '撤回了一条消息，撤回的内容为：'
                itchat.send(tip, 'filehelper')  # 发信息给文件助手
                # itchat.send(tip, toUserName)  # 发送给撤回对象
                filename = "@fil@"+content  # 找出要发出的文件，该格式为itchat的格式
                itchat.send(filename, 'filehelper')  # 发送附件信息
                # itchat.send(filename, toUserName)  # 发送给撤回对象
        except Exception as err:
            print(err)
            print('网络卡慢')
        data_dict.pop(old_msg_id)  # 删除旧字典信息


def main():  # 占位符
    try:  # 进行异常处理
        itchat.auto_login(hotReload=True)  # 微信登陆,hotReload=True避免重复扫码 ---》 生成一份文件（pkl）来记载用户登陆信息
    except Exception as err:
        print('您的微信账号存在异常状态，无法正常使用')
        # engine = pyttsx3.init()
        # engine.say('您的微信账号出现异常，无法使用')
        # engine.runAndWait()
    itchat.run()  # 微信运行起来


if __name__ == '__main__':  # 内建变量 这个操作import到其他脚本中不会被执行，__name__是python的内置的系统变量
    main()  # 调用函数
# data = dir(__builtins__)
# 查看当前文件中内置全局变量以字典方式返回内置全局变量
# print(vars())
'''
这个语句是我最近接触到的，正好写进这个程序运用一下，它的含义是这样的：
每个python模块（python文件，也就是此处的test.py和import_test.py）都包含内置的变量__name__,当运行模块被执行的时候，
__name__等于文件名（包含了后缀.py）；如果import到其他模块中，则__name__等于模块名称（不包含后缀.py）。
而“__main__”等于当前执行文件的名称（包含了后缀.py）。进而当模块被直接执行时，__name__ == 'main'结果为真。
'''