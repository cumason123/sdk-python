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

import json

from cloudevents.sdk.http_events import Event
from cloudevents.tests.data import http_event_ce_json as test_data
from cloudevents.tests.data import http_event_test_headers as test_headers

from sanic import response
from sanic import Sanic


app = Sanic(__name__)


def post(url, headers, json):
    return app.test_client.post(url, headers=headers, data=json)


@app.route("/event", ["POST"])
async def echo(request):
    event = Event(dict(request.headers), request.body)
    return response.text(event.data, headers=event.headers)


def test_invalid_binary_headers():
    for i in range(len(test_headers)):
        headers = test_headers[i]
        try:
            _ = Event(headers, test_data)
        except (TypeError, NotImplementedError):
            continue
        assert False


def test_emit_binary_event():
    headers = {
        "ce-id": "my-id",
        "ce-source": "<event-source>",
        "ce-type": "cloudevent.event.type",
        "ce-specversion": "0.2"
    }
    event = Event(headers, test_data)
    _,r = app.test_client.post(
        "/event", 
        headers=event.headers, 
        data=json.dumps(event.data)
    )
    body = json.loads(r.body)
    for key in test_data:
        assert body[key] == test_data[key]
    for key in headers:
        assert r.headers[key] == headers[key]
    assert r.status_code == 200
