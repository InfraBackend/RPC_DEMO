import itcast_pb2_grpc
import itcast_pb2
import grpc
from concurrent import futures
import time


# 实现被调用的方法的具体代码
class DemoServicer(itcast_pb2_grpc.DemoServicer):
    def __init__(self):
        self.city_subjects_db = {
            'beijing': ['python', 'c++', 'go', 'java', 'php'],
            'shanghai': ['python', 'c++', 'go', 'java'],
            'wuhan': ['python', 'java', 'php']
        }
        self.answers = list(range(10))

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
                # 通过设置响应状态码和描述字符串来达到抛出异常的目的
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('cannot divide by 0')
                return itcast_pb2.Result()
            result = request.num1 // request.num2
            return itcast_pb2.Result(val=result)
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('invalid operation')
            return itcast_pb2.Result()

    def GetSubjects(self, request, context):
        city = request.name
        subjects = self.city_subjects_db.get(city)
        for subject in subjects:
            yield itcast_pb2.Subject(name=subject)

    def Accumulate(self, request_iterator, context):
        sum = 0
        for request in request_iterator:
            sum += request.val
        return itcast_pb2.Sum(val=sum)

    def GuessNumber(self, request_iterator, context):
        for request in request_iterator:
            if request.val in self.answers:
                yield itcast_pb2.Answer(val=request.val, desc='bingo')


# 开启服务器，对外提供rpc调用
def serve():
    # 创建服务器对象, 多线程的服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册实现的服务方法到服务器对象中
    itcast_pb2_grpc.add_DemoServicer_to_server(DemoServicer(), server)

    # 为服务器设置地址
    server.add_insecure_port('127.0.0.1:8888')

    # 开启服务
    print('服务器已开启')
    server.start()

    # 关闭服务
    # 使用 ctrl+c 可以退出服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()