# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import typing
import json
import requests
import io
from cloudevents.sdk.event import base
from cloudevents.sdk import marshaller
from cloudevents.sdk import converters
from cloudevents.sdk.event import v1
class BinaryEvent(base.BaseEvent):
    # TODO: SUPPORT structured calls
    def __init__(self, headers: dict, data: typing.IO, f: typing.Callable = lambda x: x):
        required_fields = ['ce-id', 'ce-source', 'ce-type', 'ce-specversion']
        optional_fields = ['content-type', 'content-encoding', 'schema', 'subject', 'time']

        for field in required_fields:
            if field not in headers:
                raise TypeError("parameter headers has no required attribute {0}".format(field))

            if not isinstance(headers[field], str):
                raise TypeError("in parameter headers attribute {0} expected type str but found type {1}".format(
                    field, type(headers[field])
                ))

        for field in optional_fields:
            if field in headers and not isinstance(headers[field], str):
                raise TypeError("in parameter headers attribute {0} expected type str but found type {1}".format(
                    field, type(headers[field])
                ))

        self.m = marshaller.NewDefaultHTTPMarshaller()
        self.event_handler = v1.Event()
        self.m.FromRequest(self.event_handler, headers, data, f)
    
    def emit(self, url: str, binary: bool = True) -> None:
        if binary:
            self.run_binary(url)
        else:
            self.run_structured(url)
    
    # TODO: Support other HTTP Methods
    def run_binary(self, url: str) -> requests.models.Response:
        binary_headers, binary_data = self.m.ToRequest(
            self.event_handler, converters.TypeBinary, json.dumps
        )
        response = requests.post(
            url, headers=binary_headers, data=binary_data
        )
        return response

    def run_structured(self, url):
        structured_headers, structured_data = self.m.ToRequest(
            event, converters.TypeStructured, json.dumps
        )
        response = requests.post(url,
            headers=structured_headers,
            data=structured_data.getvalue()
        )
        return response
