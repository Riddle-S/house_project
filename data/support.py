import random


#随机生成电话号码
def create_telephone():
    list = [
        '139', '138', '137', '136', '135', '134', '159', '158', '157', '150',
        '151', '152', '188', '187', '182', '183', '184', '178', '130', '131',
        '132', '156', '155', '186', '185', '176', '133', '153', '189', '180',
        '181', '177'
    ]
    str = '0123456789'
    return random.choice(list) + "".join(random.choice(str) for i in range(8))


#随机生成8位用户ID
def create_id():
    return str(random.randint(10000000, 99999999))


#随机生成6位salt
def create_salt():
    return str(random.randint(100000, 999999))


"""
判断密码强度
1.0:密码长度大于8
    包含数字
    包含字母
"""


def check_number_exit(password):
    """
    判断是否含有数字
    """
    for x in password:
        if x.isnumeric():
            return True
    return False


def check_letter_exit(password):
    """
    判断是否含有字母
    """
    for x in password:
        if x.isalpha():
            return True
    return False


def check_password(password):
    """
    主函数
    """
    password_str = password
    #规则1：密码长度至少8位
    if len(password_str) < 8:
        return 1
    #规则2：包含数字
    if check_number_exit(password_str) == False:
        return 2
    #规则3：包含字母
    if check_letter_exit(password_str) == False:
        return 3
    #检测通过
    return 0
