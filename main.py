import json
import os

from inputdata import ORG_ID, MEMBER_IDS, EVENT_IDS, CREDIT_NOTE, CREDIT_AMOUNT, AUTH_USERNAME
from models import Credit
from msrserver import MsrServer


def main():
    server = MsrServer(ORG_ID, AUTH_USERNAME, os.environ['MSR_PASSWORD'])

    paid_event_member_ids: dict[str, list[str]] = {}
    for event_name, event_id in EVENT_IDS.items():
        paid_event_member_ids[event_id] = server.get_paid_event_member_ids(event_id)

    for name, member_id in MEMBER_IDS.items():
        print(f'### Processing {name} ({member_id}) ###')
        all_existing_credits = server.get_credits_for_user(member_id).credits

        for event_name, event_id in EVENT_IDS.items():
            credits_for_event = [
                credit
                for credit in all_existing_credits
                if credit.eventId == event_id
            ]
            paid = member_id in paid_event_member_ids.get(event_id)
            process_event(server, name, member_id, event_name, event_id, paid, credits_for_event)


def process_event(
        server: MsrServer,
        name: str,
        member_id: str,
        event_name: str,
        event_id: str,
        paid: bool,
        credits_for_event: list[Credit]
) -> None:
    print(f'  - Processing credit for {event_name} (silence implies no action taken)')

    existing_credit_count = len(credits_for_event)
    if existing_credit_count == 0:
        if not paid:
            print(f'\tNo credit for {event_name}. Creating...')
            server.create_credit(member_id, event_id, CREDIT_AMOUNT, CREDIT_NOTE)
    elif existing_credit_count == 1 and not paid:
        credit = credits_for_event[0]
        if CREDIT_NOTE != credit.note or float(CREDIT_AMOUNT) != float(credit.amount):
            recreate_credit(server, name, member_id, event_id, credit)
    else:
        clear_extra_credits(server, name, member_id, credits_for_event)
        if paid:
            print(f'\t{name} already paid for {event_name} but had additional credit(s). Additional credit(s) deleted.')
        else:
            print(f'\tAll credits for {name} / {event_name} deleted.')
            server.create_credit(member_id, event_id, CREDIT_AMOUNT, CREDIT_NOTE)
            print(f'\tRecreated one credit for {event_name}')


def recreate_credit(server: MsrServer, name: str, member_id: str, event_id: str, credit: Credit) -> None:
    if credit.redeemed:
        print(json.dumps(credit, indent=2))
        raise Exception(f'Bad credit has been redeemed by {name}!')
    else:
        print('\tExisting credit configured incorrectly. Deleting and recreating...')
        server.delete_credit(member_id, credit)
        server.create_credit(member_id, event_id, CREDIT_AMOUNT, CREDIT_NOTE)


def clear_extra_credits(server: MsrServer, name: str, member_id: str, credits_for_event: list[Credit]) -> None:
    for credit in credits_for_event:
        if credit.redeemed:
            print(json.dumps(credit, indent=2))
            raise Exception(f'Bad credit has been redeemed by {name}!')
        else:
            server.delete_credit(member_id, credit)


if __name__ == '__main__':
    main()
