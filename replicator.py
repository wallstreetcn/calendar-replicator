# -*- coding: utf-8 -*-

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)
from emitter import Emitter
import json
import settings

def main():
    print 'Replicator Started'
    io = Emitter(dict(
        host=settings.SOCKETIO_SETTINGS['host'],
        port=settings.SOCKETIO_SETTINGS['port']
        )).Of(settings.SOCKETIO_SETTINGS['namespace'])
    stream = BinLogStreamReader(connection_settings=settings.MYSQL_SETTINGS,
                                server_id=3,
                                blocking=True,
                                resume_stream=True,
                                only_events=[UpdateRowsEvent],
                                only_tables=[settings.DB_SETTINGS['source_table']])

    for binlogevent in stream:
         for row in binlogevent.rows:
             vals = row["after_values"]
             print 'Updated rows for ' + json.dumps(vals)
             io.Emit('update', json.dumps(vals))

    stream.close()

if __name__ == "__main__":
    main()

