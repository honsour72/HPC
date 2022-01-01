import grpc
import asyncio
import data_pb2
import data_pb2_grpc

__all__ = [
    'client_streaming_method'
]

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1
PASSWORDS = ['123', '456', 'qwerty123456']


async def client_streaming_method(stub, data):
    print "--------------Call ClientStreamingMethod Begin--------------"

    def request_messages():
        for i in range(len(data)):
            request = data_pb2.Request(
                client_id=CLIENT_ID,
                request_data=(data[i]))
            yield request

    response = await stub.ClientStreamingMethod(request_messages())
    print "Response from server {}: {}".format(response.server_id, response.response_data)
    print "--------------Call ClientStreamingMethod Over---------------"


async def main():
    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)
        await client_streaming_method(stub, PASSWORDS)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
