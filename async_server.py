try:
    from concurrent import futures
except ImportError:
    import features as futures
import asyncio
import grpc
import data_pb2
import data_pb2_grpc
import zipfile


# Константы
__all__ = 'Server'
SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


# Созданный класс сервера наследует класс демо-сервера из модуля data_pb2_grpc. В родительском классе инициализирутся
# "методы" в соответствии с буфером протокола (файл формата .proto)
# Здесь же одноимённый метод ClientStreamingMethod выполнится только в случае вызова его со стороны клиента
class Server(data_pb2_grpc.GRPCDemoServicer):
    async def ClientStreamingMethod(self, request_iterator):
        """
        Печатает сообщение в терминале сервера как только вызывается на стороне клиента, затем парсит запрос-генератор
        при помощи функции unzip_file, входяящим аргументом которой является пароль к архиву, отправляемый клиентом.
        В случае успешной распаковки - в качестве теста - возвращает содержимое одноимённого текстового файла,
        находящегося в архиве иначе сообщение об успешном завершении работы метода
        :param request_iterator: Генератор, возвращаемый (отправляемый) клиентом
        :return: ответ сервера (response) - экземпляр класса
        """
        print "ClientStreamingMethod called by client..."
        async for request in request_iterator:
            data = await unzip_file(request.request_data)
            response_data = data if data else "Python server ClientStreamingMethod ok"
        response = data_pb2.Response(
            server_id=SERVER_ID,
            response_data=response_data)
        return response


async def unzip_file(password, filename='win.7z'):
    """
    Функция получает пароль и пытается распаковать архив.
    В случае успеха - возвращает содержимое файла иначе - None
    :param password: строка - предполагаемый пароль к архиву
    :param filename: строка - название архива, по умолчанию win.7z
    :return:
    """
    archive = zipfile.ZipFile(filename)
    try:
        archive.extractall(pwd=password)
        filename = 'win.txt'
    except:
        return

    with open(filename) as file:
        return file.read()


async def main():
    """
    Основная функция по работе модуля сервера. Посредством модуля grpc инициализирует глобальный сервер server,
    через который в дальнейшем класс Sever() настоящего модуля будет пробрасывать свои методы
    Основное отличие - неблокирующий метод реализации при помощи asyncio
    :return: None
    """
    server = grpc.aio.server()  # здесь уже при инициализации глобального сервера вызывается подмодуль aio
    # метод add_GRPCDemoServicer_to_server используется для добавления локального сервера (первый аргумент) в глобальный
    # (второй аргумент)
    data_pb2_grpc.add_GRPCDemoServicer_to_server(Server(), server)
    server.add_insecure_port(SERVER_ADDRESS)  # добавляем порт из констант
    print "Server is working . . ."
    await server.start()
    # метод wait_for_termination используется для отлавливания всех запросов клиента к данному серверу
    await server.wait_for_termination()


# вызов основной функции main при помощи метода run_until_complete событий цикла (event loop) asyncio
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
