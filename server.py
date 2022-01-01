try:
    from concurrent import futures
except ImportError:
    import features as futures

import grpc

import data_pb2
import data_pb2_grpc

import zipfile

__all__ = 'Server'
SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class Server(data_pb2_grpc.GRPCDemoServicer):
    def ClientStreamingMethod(self, request_iterator, context):
        print("ClientStreamingMethod called by client...")
        for request in request_iterator:
            data = unzip_file(request.request_data)
            response_data = data if data else "Python server ClientStreamingMethod ok"
        response = data_pb2.Response(
            server_id=SERVER_ID,
            response_data=response_data)
        return response


def unzip_file(password, filename='win.7z'):
    archive = zipfile.ZipFile(filename)
    try:
        archive.extractall(pwd=password)
        filename = 'win.txt'
    except:
        return

    with open(filename) as file:
        return file.read()


def main():
    server = grpc.server(futures.ThreadPoolExecutor())

    data_pb2_grpc.add_GRPCDemoServicer_to_server(Server(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    print "Server is working . . ."
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
