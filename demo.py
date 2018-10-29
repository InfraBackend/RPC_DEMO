# -*- coding: utf-8 -*-
# 1 Unary RPC
# 服务器
import itcast_pb2_grpc
import itcast_pb2
import grpc
from concurrent import futures
import time


class DemoServicer(itcast_pb2_grpc.DemoServicer):

    def Calculate(self, request, context):
        if request.op == itcast_pb2.Work.ADD:
            result = request.num1 + request.num2
            return itcast_pb2.Result(val=result)
        elif request.op == itcast_pb2.Work.SUBTRACT:
            result = request.num1 - request.num2
            return itcast_pb2.Result(val=result)
        elif request.op == itcast_pb2.Work.MULTIPLY:
            result = request.num1 * request.num2
            return itcast_pb2.Result(val=result)
        elif request.op == itcast_pb2.Work.DIVIDE:
            if request.num2 == 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('cannot divide by 0')
                return itcast_pb2.Result()
            result = request.num1 // request.num2
            return itcast_pb2.Result(val=result)
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('invalid operation')
            return itcast_pb2.Result()


def serve():
    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 注册本地服务
    itcast_pb2_grpc.add_DemoServicer_to_server(DemoServicer(), server)
    # 监听端口
    server.add_insecure_port('127.0.0.1:8888')
    # 开始接收请求进行服务
    server.start()
    # 使用 ctrl+c 可以退出服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
# 客户端
import grpc
import itcast_pb2_grpc
import itcast_pb2


def invoke_calculate(stub):
    work = itcast_pb2.Work()
    work.num1 = 100
    work.num2 = 50
    work.op = itcast_pb2.Work.ADD
    result = stub.Calculate(work)
    print('100+50={}'.format(result.val))

    work.op = itcast_pb2.Work.MULTIPLY
    result = stub.Calculate(work)
    print('100*50={}'.format(result.val))

    work.op = itcast_pb2.Work.DIVIDE
    result = stub.Calculate(work)
    print('100//50={}'.format(result.val))

    work.num2 = 0
    work.op = itcast_pb2.Work.DIVIDE
    try:
        result = stub.Calculate(work)
        print('100//0={}'.format(result.val))
    except grpc.RpcError as e:
        print('{}:{}'.format(e.code(), e.details()))


def run():
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        stub = itcast_pb2_grpc.DemoStub(channel)
        invoke_calculate(stub)


if __name__ == '__main__':
    run()
# 2 Server Streaming RPC
# 服务器
class DemoServicer(itcast_pb2_grpc.DemoServicer):
    def __init__(self):
        self.city_subject_db = {
            'beijing': ['python', 'c++', 'go', '测试', '运维', '产品经理', 'java', 'php'],
            'shanghai': ['python', 'c++', 'go', '测试', '运维', 'java', 'php'],
            'wuhan': ['python', 'java', '测试']
        }

    def GetCitySubjects(self, request, context):
        city = request.name
        subjects = self.city_subject_db.get(city)
        for subject in subjects:
            yield itcast_pb2.Subject(name=subject)
# 客户端
def invoke_get_city_subjects(stub):
    city = itcast_pb2.City(name='beijing')
    subjects = stub.GetCitySubjects(city)
    for subject in subjects:
        print(subject.name)
# 3 Client Streaming RPC
# 服务器
class DemoServicer(itcast_pb2_grpc.DemoServicer):
    def Accumulate(self, request_iterator, context):
        sum = 0
        for num in request_iterator:
            sum += num.val

        return itcast_pb2.Sum(val=sum)
# 客户端
def generate_delta():
    for _ in range(10):
        num = random.randint(1, 100)
        print(num)
        yield itcast_pb2.Delta(val=num)


def invoke_accumulate(stub):
    delta_iterator = generate_delta()
    sum = stub.Accumulate(delta_iterator)
    print('sum={}'.format(sum.val))
# 4 Bidirectional Streaming RPC
# 服务器
class DemoServicer(itcast_pb2_grpc.DemoServicer):
    def __init__(self):
        self.answers = list(range(10))

    def GuessNumber(self, request_iterator, context):
        for num in request_iterator:
            if num.val in self.answers:
                yield itcast_pb2.Answer(val=num.val, desc='bingo')
# 客户端
def generate_num():
    for _ in range(10):
        num = random.randint(1, 20)
        print(num)
        yield itcast_pb2.Number(val=num)


def invoke_guess_number(stub):
    number_iterator = generate_num()
    answers = stub.GuessNumber(number_iterator)
    for answer in answers:
        print('{}: {}'.format(answer.desc, answer.val))