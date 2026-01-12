import logging
from typing import Optional
from flask import has_request_context
from flask import request


class CustomLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if has_request_context():
            # Type annotations not supported on dynamic attributes
            record.url = request.url
            record.method = request.method  
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.method = None
            record.remote_addr = None
        
        return super().format(record)