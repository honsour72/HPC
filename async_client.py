# Copyright 2019 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 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
"""The example of four ways of data transmission using gRPC in Python."""

import os
import time

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
    print("--------------Call ClientStreamingMethod Begin--------------")

    def request_messages():
        res = []
        for i in range(len(data)):
            request = data_pb2.Request(
                client_id=CLIENT_ID,
                request_data=(data[i]))
            yield request
            # res.append(request)
        # return res

    # print("--------------Call ClientStreamingMethod Over---------------")
    # return stub.ClientStreamingMethod(request_messages())
    # response = stub.ClientStreamingMethod(request_messages())
    response = await stub.ClientStreamingMethod(request_messages())
    # response = stub.get_client_stream(request_messages())
    print("Response from server {}: {}".format(response.server_id, response.response_data))
    # print("Response from server {}".format(response))
    # print(dir(response))
    # print("resp from server(%d), the message=%s" %
    #       (response.server_id, response.response_data))
    print("--------------Call ClientStreamingMethod Over---------------")



async def main():
    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)

        # simple_method(stub, filename)

        await client_streaming_method(stub, PASSWORDS)
        # response = await client_streaming_method(stub, PASSWORDS)
        # print("Response from server {}".format(response))
        # server_streaming_method(stub)

        # bidirectional_streaming_method(stub)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
