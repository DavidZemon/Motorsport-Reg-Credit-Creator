from marshmallow import Schema, fields, post_load


class RecordSet:
    total: int
    remaining: int
    page: int

    def __init__(self, total: int, remaining: int, page: int) -> None:
        super().__init__()
        self.total = total
        self.remaining = remaining
        self.page = page


class RecordSetSchema(Schema):
    total = fields.Number()
    remaining = fields.Number()
    page = fields.Number()

    # noinspection PyUnusedLocal
    @post_load
    def make_record_set(self, data, **kwargs):
        return RecordSet(**data)


# noinspection PyPep8Naming,PyShadowingBuiltins
class Credit:
    eventType: str
    created: str
    amount: float
    note: str
    expires: str
    eventId: str
    id: str
    redeemed: str

    def __init__(
            self,
            eventType: str,
            created: str,
            amount: float,
            note: str,
            expires: str,
            eventId: str,
            id: str,
            redeemed: str,
    ) -> None:
        super().__init__()
        self.eventType = eventType
        self.created = created
        self.amount = amount
        self.note = note
        self.expires = expires
        self.eventId = eventId
        self.id = id
        self.redeemed = redeemed


class CreditSchema(Schema):
    eventType = fields.String()
    created = fields.String()
    amount = fields.Number()
    note = fields.String()
    expires = fields.String()
    eventId = fields.String()
    id = fields.String()
    redeemed = fields.String()

    # noinspection PyUnusedLocal
    @post_load
    def make_credit(self, data, **kwargs):
        return Credit(**data)


# noinspection PyShadowingBuiltins
class UserCreditsResponse:
    recordset: RecordSet
    credits: list[Credit]

    def __init__(self, recordset: RecordSet, credits: list[Credit]) -> None:
        super().__init__()
        self.recordset = recordset
        self.credits = credits


# noinspection PyTypeChecker
class UserCreditsResponseSchema(Schema):
    recordset = fields.Nested(RecordSetSchema)
    credits = fields.List(fields.Nested(CreditSchema))

    # noinspection PyUnusedLocal
    @post_load
    def make_user_credits_response(self, data, **kwargs):
        return UserCreditsResponse(**data)
