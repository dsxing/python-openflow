"""The controller has requested to be notified when flows time out."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.foundation.base import GenericMessage
from pyof.v0x01.foundation.basic_types import (PAD, UBInt8, UBInt16, UBInt32,
                                               UBInt64)

__all__ = ('FlowRemoved', 'FlowRemovedReason')

# Enums


class FlowRemovedReason(Enum):
    """Why the flow was removed."""

    #: Flow idle time exceeded idle_timeout
    OFPRR_IDLE_TIMEOUT = 1
    #: Time exceeded hard_timeout
    OFPRR_HARD_TIMEOUT = 2
    #: Evicted by a DELETE flow mod
    OFPRR_DELETE = 3


# Classes
class FlowRemoved(GenericMessage):
    """Flow removed (datapath -> controller)."""

    #: :class:`~.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_FLOW_REMOVED)
    #: :class:`~.flow_match.Match`: OpenFlow Header
    match = Match()
    cookie = UBInt64()

    priority = UBInt16()
    reason = UBInt8(enum_ref=FlowRemovedReason)
    #: Align to 32-bits.
    pad = PAD(1)

    duration_sec = UBInt32()
    duration_nsec = UBInt32()

    idle_timeout = UBInt16()
    #: Align to 64-bits.
    pad2 = PAD(2)
    packet_count = UBInt64()
    byte_count = UBInt64()

    def __init__(self, xid=None, match=None, cookie=None, priority=None,
                 reason=None, duration_sec=None, duration_nsec=None,
                 idle_timeout=None, packet_count=None, byte_count=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): OpenFlow Header's xid.
            match (Match): Fields' description.
            cookie (int): Opaque controller-issued identifier.
            priority (int): Priority level of flow entry.
            reason (FlowRemovedReason): Why the flow was removed.
            duration_sec (int): Time the flow was alive in seconds.
            duration_nsec (int): Time the flow was alive in nanoseconds in
                addition to duration_sec.
            idle_timeout (int): Idle timeout from original flow mod.
            packet_count (int): Number of packets.
            byte_count (int): Byte count.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.match = match
        self.cookie = cookie
        self.priority = priority
        self.reason = reason
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.idle_timeout = idle_timeout
        self.packet_count = packet_count
        self.byte_count = byte_count
