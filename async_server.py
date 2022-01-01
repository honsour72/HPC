try:
    from concurrent import futures
except ImportError:
    import features as futures

import asyncio
import grpc

import data_pb2
import data_pb2_grpc

__all__ = 'Server'

import zipfile

SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class Server(data_pb2_grpc.GRPCDemoServicer):
    async def ClientStreamingMethod(self, request_iterator, context):
        print "ClientStreamingMethod called by client..."
        async for request in request_iterator:
            data = await unzip_file(request.request_data)
            response_data = data if data else "Python server ClientStreamingMethod ok"
        response = data_pb2.Response(
            server_id=SERVER_ID,
            response_data=response_data)
        return response


async def unzip_file(password, filename='win.7z'):
    archive = zipfile.ZipFile(filename)
    try:
        archive.extractall(pwd=password)
        filename = 'win.txt'
    except:
        return

    with open(filename) as file:
        return file.read()


async def main():
    server = grpc.aio.server()
    data_pb2_grpc.add_GRPCDemoServicer_to_server(Server(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    print "Server is working . . ."
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
