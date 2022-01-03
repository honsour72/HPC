import grpc
import asyncio
import data_pb2
import data_pb2_grpc


# Константы
__all__ = ['client_streaming_method']
SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1
PASSWORDS = ['123', '456', 'qwerty123456']


async def client_streaming_method(stub, data):
    """
    Принимает стаб сервиса и массив паролей, через первый вызывает метод передачи stream-unary,
    когда клиент в запросе отдаёт генератор (то есть множество) а сервер врзвращает один результат
    Печатает в терминале клиента сообщение о вызове метрда, ответ сервера на посланные данные и знак когда работа метода
    будет окончана
    :param stub: стаб - это потоковый буфер выступающий в роли связующего моста как между клиентом и "сервисом"
    так и между локальным сервером и "сервисом"
    :param data: массив паролей
    :return: None
    """
    print "--------------Call ClientStreamingMethod Begin--------------"

    def request_messages():
        for i in range(len(data)):
            request = data_pb2.Request(
                client_id=CLIENT_ID,
                request_data=(data[i]))
            yield request

    # Вот тут происходит вызов серверного метода, переданного в настоящий модуль благодаря stub'у
    response = await stub.ClientStreamingMethod(request_messages())
    print "Response from server {}: {}".format(response.server_id, response.response_data)
    print "--------------Call ClientStreamingMethod Over---------------"


async def main():
    """
    Основная функция проекта, работающая без блокировки посредством метода insecure_channel по серверному адресу
    инициализирует канал, в котором уже создаётся stub и вызывается клиентский метод, посылающий на сервер пароли
    :return: None
    """
    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)
        await client_streaming_method(stub, PASSWORDS)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
