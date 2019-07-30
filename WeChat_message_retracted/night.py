# pip install itchat
# pip install pyttsx3
# 导入第三方库
import itchat
import re
import pyttsx3
"""
从简到繁 从易到难
微信专题之消息防撤回
反问老板问清楚你的需求
微信消息防撤回  我给你发消息 文字 照片 视频 语音撤回了
分析  大概怎么去实现
主业务逻辑 不要慌   加入我大量的开发经验 和  职场套路
消息撤回了==消息丢失了？
 备份  还怕什么丢了
只要备份了消息 遇到撤回，我就把备份里面的消息给拿出来
"""

# 定义一个字典
data_dict = dict()
"""
作用域分为全局和局部
函数体内的为局部，只能在本函数体内使用
全体的可以在任意位置使用
简单的举例：你自己的房间电脑只能你使用，而放在客厅的电脑，谁都可以使用
声明就是给你一把钥匙，允许你去更改它

函数体内获取函数体外的变量的方式：作为参数传递和全局作用域
尽量避免全局变量来传递
容易引起混乱，出错，也不利于代码的可读性
函数不可能总处于被动用的状态，而全局变量就需要占用空间，浪费空间
"""
# 表示只要接收到文本消息就自动调用下发的函数
# 增加语音，照片，视频的信息接收


@itchat.msg_register(['Text', 'Picture', 'Recording', 'Video'])
def message(msg):
    # 在这里存信息，把所有信息都存起来.
    print(msg)
    # 改写全局变量
    global data_dict
    # 谁发的消息 因为msg['FromUserName']根本看不懂 所以获取昵称
    name = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    print(name)
    # 唯一不重复的就是ID 相当于我们人类的身份证
    id = msg['MsgId']
    # 获取消息的类型
    type = msg['Type']
    if type =='Text':
        # 提取出文本消息内容 去除左右两边的空格
        text = msg['Text'].strip()
        # 获取发送的文字内容  去除左右空格
        content = text
    else:
    #itchat的附件下载方法存储在msg的Text键中
        # 将文件下载下来
        msg['Text'](msg['FileName'])
        # 获取下载好的文件名
        content = msg['FileName']
    # 把信息存入内容
    data_dict[id] = {'name': name, 'content': content, 'type': type}


# 表示只要接收到微信通知就自动调用下发的函数
@itchat.msg_register('Note')
def notice(msg):
    print(msg)
    # 在这里读取信息，当发现有撤回消息的通知就读取消息
    # 判断是不是撤回消息 （微信通知，除了消息撤回还有红包等等通知）
    # 细心，因为常用的有简体中文和繁体中文
    if '撤回了一条消息' in msg['Text'] or '你已回收一條訊息' in msg['Text']:
        try:
            # 利用正则找出对应的内容 表示找出正则表达式中的第一个括号内的内容
            old_msg_id = re.search('\<msgid\>(.*?)\<\/msgid\>', msg['Content']).group(1)
            # 找出昵称
            name = data_dict[old_msg_id]['name']
            # 找出内容
            content = data_dict[old_msg_id]['content']
            # 做判断  找出类型
            type = data_dict[old_msg_id]['type']
            # 反摩擦
            # 找出是谁发的
            # 根据备注名得到朋友的UserName
            toUserName = itchat.search_friends(nickName=name)[0]['UserName']
            if type == 'Text':
                # 拼接消息，发送给文件助手
                tip = name + '撤回了一条消息，内容为：' + content
                itchat.send(tip, 'filehelper')
                itchat.send(tip, toUserName)
            else:
                # 拼接消息，发送给文件助手
                tip = name + '撤回了一条消息，内容为：'
                itchat.send(tip, 'filehelper')
                itchat.send(tip, toUserName)
                # 找出要发送的文件 该格式为itchat的格式
                filename = "@fil@"+content
                # 发送附件消息
                itchat.send(filename, 'filehelper')
                itchat.send(filename, toUserName)
        except Exception as err:
            print(err)
            print('网络卡慢')
        # 删除字典旧信息
        data_dict.pop(old_msg_id)

def main():
    # 异常处理
    try:
        # 先登录微信  热加载 避免重复扫码
        # 生成一份文件  这份文件就是用来记录登录信息
        itchat.auto_login(hotReload=True)
    except Exception as err:
        print('您的微信账号出现异常，无法使用')
        # engine = pyttsx3.init()
        # engine.say('您的微信账号出现异常，无法使用')
        # engine.runAndWait()
    # 才能够使用微信
    # 让微信运行起来  见名知义
    itchat.run()
# __name__是python的内置的系统变量
# 作为程序主入口
# 主线
if __name__=='__main__':
    main()
# 内建变量
# data = dir(__builtins__)
# 查看当前文件中内置全局变量以字典方式返回内置全局变量
# print(vars())
# str = 'rrr123abc456'
# print(re.search('rrr([0-9]*)([a-z]*)([0-9]*)',str).group(0))
# print(re.search('rrr([0-9]*)([a-z]*)([0-9]*)',str).group(1))
# print(re.search('rrr([0-9]*)([a-z]*)([0-9]*)',str).group(2))
# print(re.search('rrr([0-9]*)([a-z]*)([0-9]*)',str).group(3))