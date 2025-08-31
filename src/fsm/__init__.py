"""
Simple FSM for HTTP Status Codes
===============================

A digit-by-digit finite state machine for HTTP status codes.
"""

from .http_fsm import HTTPCodeFSM

__all__ = ['HTTPCodeFSM']
