import grpc
import itcast_pb2_grpc
import itcast_pb2
import random


def invoke_calculate(stub):
    work = itcast_pb2.Work()
    work.num1 = 100
    work.num2 = 20
    work.op = itcast_pb2.Work.ADD
    result = stub.Calculate(work)
    print('100 + 20 = {}'.format(result.val))

    work.op = itcast_pb2.Work.SUBTRACT
    result = stub.Calculate(work)
    print('100 - 20 = {}'.format(result.val))

    work.op = itcast_pb2.Work.MULTIPLY
    result = stub.Calculate(work)
    print('100 * 20 = {}'.format(result.val))

    work.op = itcast_pb2.Work.DIVIDE
    result = stub.Calculate(work)
    print('100 // 20 = {}'.format(result.val))

    work.num2 = 0
    try:
        result = stub.Calculate(work)
        print('100 // 20 = {}'.format(result.val))
    except grpc.RpcError as e:
        print('{}: {}'.format(e.code(), e.details()))


def invoke_get_subjects(stub):
    city = itcast_pb2.City(name='beijing')
    subjects = stub.GetSubjects(city)
    for subject in subjects:
        print(subject.name)


def generate_delta():
    for _ in range(10):
        delta = random.randint(1, 100)
        print(delta)
        yield itcast_pb2.Delta(val=delta)


def invoke_accumulate(stub):
    delta_iterator = generate_delta()
    sum = stub.Accumulate(delta_iterator)
    print('sum={}'.format(sum.val))


def generate_number():
    for _ in range(10):
        number = random.randint(1, 20)
        print(number)
        yield itcast_pb2.Number(val=number)


def invoke_guess_number(stub):
    number_iterator = generate_number()
    answers = stub.GuessNumber(number_iterator)
    for answer in answers:
        print('{}: {}'.format(answer.desc, answer.val))


def run():
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        # 创建辅助客户端调用的stub对象
        stub = itcast_pb2_grpc.DemoStub(channel)

        # invoke_calculate(stub)
        # invoke_get_subjects(stub)
        # invoke_accumulate(stub)
        invoke_guess_number(stub)


if __name__ == '__main__':
    run()