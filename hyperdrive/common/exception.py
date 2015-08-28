#!/usr/bin/env python
# This files contains some custom defined exceptions.

import webob.exc
import json


class Fault(webob.exc.HTTPException):
    """Wrap webob.exc.HTTPException to provide API friendly response."""

    _fault_names = {
        400: "badRequest",
        401: "unauthorized",
        403: "forbidden",
        404: "itemNotFound",
        405: "badMethod",
        409: "conflictingRequest",
        413: "overLimit",
        415: "badMediaType",
        429: "overLimit",
        501: "notImplemented",
        503: "serviceUnavailable"
    }

    def __init__(self, exception):
        """Create a Fault for the given webob.exc.exception."""
        self.exception = exception
        self.status = exception.status_int
        self.message = self._fault_names.get(self.status)

    @webob.dec.wsgify
    def __call__(self, req):
        """Generate a WSGI response based on the exception passed to ctor."""

        # Replace the body with fault details.
        content_type = 'application/json'
        body = {'status': self.status, 'message': self.message}
        self.exception.body = json.dumps(body)
        self.exception.content_type = content_type

        return self.exception

    def __str__(self):
        return self.exception.__str__()