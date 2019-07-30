#!/usr/bin/python3
# @Time      : 2019/7/3 19:14
# @Author    : 老杨
# @FileName  : test.py
# @Software  : PyCharm
"""
课题分享:微信消息防撤回
主讲老师:老杨老师
开发环境:pycharm + python3
课堂规则:
第一:不要拘泥于代码,思维远比代码重要
第二;积极和老师配合,互动.便于老师了解同学们的学习情况
"""
# 有基础1   没基础2
# 声音太小,请自行调节音量,
# 我这里一直在视频录播,同学可以加右上角助理,领取录播
# 从零开始如何完成一个项目
# 微信消息防撤回
# 第一件事:反问你的老板:  问清你的需求
# 及时拒绝不合理的需求
# 只要别人撤回了任意的消息,我都看到
# 先做思路的分析
# 微信消息 防 撤回
# 和微信打交道  获取到微信的消息内容
# 微信消息撤回
# 备份->丢失
# 2020停止维护python2  选择python3
# 2020
# 怎么学好python,用生活化的例子去理解
# 安装第三方库
# pip install itchat
# 导入第三方库
import itchat
import re
# 定义成一个全局变量
data_dict = dict()
# 只要我接受到微信的文本消息,就自动调用下方的函数
# 必须携带一个参数
# 消息注册机制
# 把所有的消息保存下来,一旦发现撤回就把消息找出来并且发送出来


@itchat.msg_register(['Text'])
def message(msg):
    # 保存消息
    print(msg)
    # 改写全局变量
    global data_dict
    # 唯一标志
    id = msg['MsgId']
    # 消息内容是什么,消息是谁发的
    # 提取出文本类消息,去掉左右空白
    content = msg['Text'].strip()
    # 谁发的消息,用户名很难看懂,想办法找出微信昵称
    # msg['FromUserName']
    # 根据微信好友的用户名提取出微信好友昵称
    name = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    # 进行保存 字典的形式
    # 新华字典
    # 会覆盖 小明 你好
    data_dict[id] = {'name':name,'content':content}

# 消息注册机制
# 接收到微信的通知


@itchat.msg_register('Note')
def notice(msg):
    print(msg)
    if '撤回了一条消息' in msg['Text']:
        old_msg_id = re.search('\<msgid\>(.*?)\<\/msgid\>', msg['Content']).group(1)
        # 找出昵称
        name = data_dict[old_msg_id]['name']
        # 找出内容
        content = data_dict[old_msg_id]['content']
        tip = name + '撤回了一条消息，内容为：' + content
        itchat.send(tip,'filehelper')
    # 删除对应的这条消息
    data_dict.pop(old_msg_id)

# 定义一个函数
def main():
    # 占位符
    # 获取到微信的消息内容
    # 你们在生活中要是用微信,第一件事是什么?
    # 登录微信
    # 参数可以避免重复扫码
    itchat.auto_login(hotReload=True)
    # bug
    # 让微信运行起来
    itchat.run()


if __name__ == '__main__':  # 内建变量
    # 调用函数
    main()

#  1
#  2  2
# 抽取一位同学
# 手机上有微信
# 你自己给自己发送一条消息,在撤回
# 666
# 微信账号出现异常
# 没有环境变量
# 一边考研  一遍学习:
# 考研 多了一个
# 考研 ->
# python
# 线上直播活动教学
# 线下有一个问题   成本太大 ->脱产学习
# 线上的话  你的时间是自由的 晚上

# 晚上进行直播互动授课
# 线上的话
#
# 高清的视频视频录播
# 线下的话
# 5
# 第一从成本角度考虑

# 从你的学习考虑
# C语言
# python
# 就业角度  C 语言
#
# 就业岗位较少  工资较低
# 人工智能 WEB 开发  爬虫
# 我们的系统课->
# 为了帮助我们零基础的学员,快速学会,学好python->可直接就业
#
# 我们的这个系统班级
# 三大
# 课程研发团队  ->
# 授课老师团队 ->
# 答题老师团队->
# 666
# 最后一个优惠
# 截止到老师下课之前
# 5个月的时间  7880
# 立即减去1000
# 6880
# 支持分期 12期的分期
##### 截止到老师下课之前
#把名额抢占下来
# 怎么才能学好python
# 2015年  人工智能 -> 2017年底
# web开发  爬虫 数据分析 自动化运维
# 科学计算
# 2019年
# 40万人才缺口
#
# 高工资 目前门槛相对较低
# PHP  10
# 立即学习
# 888
#想要立减
#学好python

# 根据就业市场决定的

# linux
# 前端知识
# python相关的编程技巧
# 数据库
# 实战项目
# 666
# 888
# 请发给我,你们在课堂上的昵称



