# -*- coding: utf-8 -*-
import struct

class DevideProtal(object):
    def args_encode(self, num1, num2=1):
        """
        将原始请求打包成二进制数据
        :param num1: 
        :param num2: 
        :return: 
        """
        name = 'devide'
        # 处理方法名
        buff = struct.pack('!I', 6)
        buff += name.encode()
        # 处理参数
        buff2 = struct.pack('!B', 1)
        buff2 += struct.pack('!i', num1)
        if num2 != 1:
            buff2 += struct.pack('!B', 1)
            buff2 += struct.pack('!i', num2)
        # 处理消息长度
        length = len(buff2)
        buff += struct.pack('!I', length)
        buff += buff2
        return buff