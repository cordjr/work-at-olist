VALID_START_CALL_PAYLOAD = {
    "id": 456,
    "type": "start",
    "timestamp": "2017-06-06T10:11:02.900Z",
    "call_id": 999,
    "source": 5598984182608,
    "destination": 559999874562
}

START_CALL_PAYLOAD_WITHOUT_SOURCE_ATTRIBUTE = {
    "id": 456,
    "type": "start",
    "timestamp": "2017-06-06T10:11:02.900Z",
    "call_id": 999,
    "destination": 559999874562
}

START_CALL_PAYLOAD_WITHOUT_DESTINATION_ATTRIBUTE = {
    "id": 456,
    "type": "start",
    "timestamp": "2017-06-06T10:11:02.900Z",
    "call_id": 999,
    "source": 5598984182608,
}

START_CALL_PAYLOAD_WITH_NULL_SOURCE = {
    "id": 456,
    "type": "start",
    "timestamp": "2017-06-06T10:11:02.900Z",
    "call_id": 999,
    "source": None,
    "destination": 559999874562

}

VALID_END_CALL_PAYLOAD = {
    "id": 456,
    "type": "end",
    "timestamp": "2017-06-06T10:11:02.900Z",
    "call_id": 999
}
