# Этот скрипт третий по важности после файла .proto и data_pb2.py. Здесь описывается родительский класс Демо-сервера и
# Сервисера (stub) при помощи которых будет реализван вызов методов сервера на стороне клиента
# После инициализируется метод  add_GRPCDemoServicer_to_server, который добавляет объект сервера к сервису.
# Это будет использовано при инициализации канала, соединяющего клиент-сервер через stub


import grpc

import data_pb2 as data__pb2


class GRPCDemoStub(object):

    def __init__(self, channel):
        self.SimpleMethod = channel.unary_unary(
            '/demo.GRPCDemo/SimpleMethod',
            request_serializer=data__pb2.Request.SerializeToString,
            response_deserializer=data__pb2.Response.FromString,
        )
        self.ClientStreamingMethod = channel.stream_unary(
            '/demo.GRPCDemo/ClientStreamingMethod',
            request_serializer=data__pb2.Request.SerializeToString,
            response_deserializer=data__pb2.Response.FromString,
        )
        self.ServerStreamingMethod = channel.unary_stream(
            '/demo.GRPCDemo/ServerStreamingMethod',
            request_serializer=data__pb2.Request.SerializeToString,
            response_deserializer=data__pb2.Response.FromString,
        )
        self.BidirectionalStreamingMethod = channel.stream_stream(
            '/demo.GRPCDemo/BidirectionalStreamingMethod',
            request_serializer=data__pb2.Request.SerializeToString,
            response_deserializer=data__pb2.Response.FromString,
        )


class GRPCDemoServicer(object):
    def SimpleMethod(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientStreamingMethod(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerStreamingMethod(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BidirectionalStreamingMethod(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GRPCDemoServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'SimpleMethod': grpc.unary_unary_rpc_method_handler(
            servicer.SimpleMethod,
            request_deserializer=data__pb2.Request.FromString,
            response_serializer=data__pb2.Response.SerializeToString,
        ),
        'ClientStreamingMethod': grpc.stream_unary_rpc_method_handler(
            servicer.ClientStreamingMethod,
            request_deserializer=data__pb2.Request.FromString,
            response_serializer=data__pb2.Response.SerializeToString,
        ),
        'ServerStreamingMethod': grpc.unary_stream_rpc_method_handler(
            servicer.ServerStreamingMethod,
            request_deserializer=data__pb2.Request.FromString,
            response_serializer=data__pb2.Response.SerializeToString,
        ),
        'BidirectionalStreamingMethod': grpc.stream_stream_rpc_method_handler(
            servicer.BidirectionalStreamingMethod,
            request_deserializer=data__pb2.Request.FromString,
            response_serializer=data__pb2.Response.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'demo.GRPCDemo', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
