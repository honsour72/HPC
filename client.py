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
"""The example of four ways of data transmission using gRPC in Python."""
import os
import time

import grpc

import data_pb2
import data_pb2_grpc

__all__ = [
    'client_streaming_method'
]

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1
PASSWORDS = ['123', '456', 'qwerty123456']


def client_streaming_method(stub, data):
    print("--------------Call ClientStreamingMethod Begin--------------")

    def request_messages():
        for i in range(len(data)):
            request = data_pb2.Request(
                client_id=CLIENT_ID,
                request_data=(data[i]))
            yield request

    response = stub.ClientStreamingMethod(request_messages())
    # response = stub.get_client_stream(request_messages())
    print("Response from server {}: {}".format(response.server_id, response.response_data))
    # print("resp from server(%d), the message=%s" %
    #       (response.server_id, response.response_data))
    print("--------------Call ClientStreamingMethod Over---------------")



def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)

        # simple_method(stub)

        client_streaming_method(stub, PASSWORDS)

        # server_streaming_method(stub)

        # bidirectional_streaming_method(stub)


if __name__ == '__main__':
    main()
