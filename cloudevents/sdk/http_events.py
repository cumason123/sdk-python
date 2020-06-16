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
import copy

import json
import typing

from cloudevents.sdk import marshaller

from cloudevents.sdk.event import base
from cloudevents.sdk.event import v1


class CloudEvent(base.BaseEvent):
    """
    Python-friendly cloudevent class supporting v1 events
    Currently only supports binary content mode CloudEvents
    """

    def __init__(
            self,
            headers: dict,
            data: any,
            f: typing.Callable = lambda x: x
    ):
        """
        Event HTTP Constructor
        :param headers: a dict with HTTP headers
            e.g. {
                "content-type": "application/cloudevents+json",
                "ce-id": "16fb5f0b-211e-1102-3dfe-ea6e2806f124",
                "ce-source": "<event-source>",
                "ce-type": "cloudevent.event.type",
                "ce-specversion": "0.2"
            }
        :type headers: dict
        :param data: a data object to be stored inside Event
        :type data: any
        :param binary: a bool indicating binary events
        :type binary: bool
        :param f: callable function for reading/extracting data
        :type f: typing.Callable
        """
        headers = {key.lower(): value for key, value in headers.items()}
        if self.is_binary_cloud_event(headers):
            # TODO: add content-type support?
            # Headers validation for binary events
            for field in base._ce_required_fields:
                ce_prefixed_field = f"ce-{field}"
                # Verify field exists else throw TypeError
                if ce_prefixed_field not in headers:
                    raise TypeError(
                        "parameter headers has no required attribute {0}"
                        .format(
                            ce_prefixed_field
                        ))

                if not isinstance(headers[ce_prefixed_field], str):
                    raise TypeError(
                        "in parameter headers attribute "
                        "{0} expected type str but found type {1}".format(
                            ce_prefixed_field, type(headers[ce_prefixed_field])
                        ))

            for field in base._ce_optional_fields:
                ce_prefixed_field = f"ce-{field}"
                if ce_prefixed_field in headers and not \
                        isinstance(headers[ce_prefixed_field], str):
                    raise TypeError(
                        "in parameter headers attribute "
                        "{0} expected type str but found type {1}".format(
                            ce_prefixed_field, type(headers[ce_prefixed_field])
                        ))
        else:
            # TODO: Support structured CloudEvents
            raise NotImplementedError

        self.headers = copy.deepcopy(headers)
        self.data = copy.deepcopy(data)
        self.marshall = marshaller.NewDefaultHTTPMarshaller()
        self.event_handler = v1.Event()
        self.marshall.FromRequest(
            self.event_handler,
            self.headers,
            self.data,
            f
        )

    def is_binary_cloud_event(self, headers):
        for field in base._ce_required_fields:
            if f"ce-{field}" not in headers:
                return False
        return True

    def __repr__(self):
        return json.dumps(
            {
                'Event': {
                    'headers': self.headers,
                    'data': self.data
                }
            },
            indent=4
        )
