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

from cloudevents.sdk.http_events import CloudEvent
from cloudevents.tests.data import test_cloudevent_body as test_data
from cloudevents.tests.data import test_cloudevent_headers as test_headers

from sanic import response
from sanic import Sanic


app = Sanic(__name__)


def post(url, headers, json):
    return app.test_client.post(url, headers=headers, data=json)


@app.route("/event", ["POST"])
async def echo(request):
    event = CloudEvent(dict(request.headers), request.body)
    return response.text(event.data, headers=event.headers)


def test_invalid_binary_headers():
    for i in range(len(test_headers)):
        headers = test_headers[i]
        try:
            # Testing error handling on CloudEvent constructor
            _ = CloudEvent(headers, test_data)
        except (TypeError, NotImplementedError):
            # CloudEvent constructor throws TypeError if missing required field
            # and NotImplementedError because structured calls aren't
            # implemented
            continue
        assert False


def test_emit_binary_event():
    headers = {
        "ce-id": "my-id",
        "ce-source": "<event-source>",
        "ce-type": "cloudevent.event.type",
        "ce-specversion": "1.0"
    }
    event = CloudEvent(headers, test_data)
    _, r = app.test_client.post(
        "/event",
        headers=event.headers,
        data=json.dumps(event.data)
    )
    body = json.loads(r.body)

    # Check response fields
    for key in test_data:
        assert body[key] == test_data[key]
    for key in headers:
        assert r.headers[key] == headers[key]
    assert r.status_code == 200


def test_missing_ce_prefix_binary_event():
    headers = {
        "ce-id": "my-id",
        "ce-source": "<event-source>",
        "ce-type": "cloudevent.event.type",
        "ce-specversion": "1.0"
    }
    for key in headers:
        val = headers.pop(key)

        # breaking prefix e.g. e-id instead of ce-id
        headers[key[1:]] = val
        try:
            # Testing error handling on CloudEvent constructor
            _ = CloudEvent(headers, test_data)
        except (TypeError, NotImplementedError):
            # CloudEvent constructor throws TypeError if missing required field
            # and NotImplementedError because structured calls aren't
            # implemented. In this instance one of the required keys should have
            # prefix e-id instead of ce-id therefore it should throw
            continue
        assert False


def test_valid_cloud_events():
    # Test creating multiple cloud events
    events_queue = []
    headers = {}
    num_cloudevents = 30
    for i in range(num_cloudevents):
        headers = {
            "ce-id": f"id{i}",
            "ce-source": f"source{i}.com.test",
            "ce-type": f"cloudevent.test.type",
            "ce-specversion": "1.0"
        }
        data = {'payload': f"payload-{i}"}
        events_queue.append(CloudEvent(headers, data))

    for i, event in enumerate(events_queue):
        headers = event.headers
        data = event.data

        assert headers['ce-id'] == f"id{i}"
        assert headers['ce-source'] == f"source{i}.com.test"
        assert data['payload'] == f"payload-{i}"
