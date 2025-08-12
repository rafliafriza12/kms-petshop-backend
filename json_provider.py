# json_provider.py
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId, Decimal128
from datetime import datetime, date
from uuid import UUID

class BSONJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal128):
            return float(o)
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, (bytes, bytearray)):
            # kalau memang perlu kirim bytes: ubah ke str (hindari untuk password)
            return o.decode("utf-8", "ignore")
        return super().default(o)
