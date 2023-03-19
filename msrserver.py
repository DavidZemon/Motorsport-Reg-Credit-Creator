import json
import sys

import requests

from models import UserCreditsResponseSchema, UserCreditsResponse, Credit, CreditSchema

BASE_URL = 'https://api.motorsportreg.com/rest'


class MsrServer:
    _session: requests.Session

    def __init__(self, org_id, username: str, password: str) -> None:
        super().__init__()
        self._session = requests.session()
        self._session.auth = (username, password)
        self._session.headers.update({
            'X-Organization-Id': org_id,
            'Accepts': 'application/json',
        })

    def get_credits_for_user(self, member_id: str) -> UserCreditsResponse:
        response = self._session.get(
            f'{BASE_URL}/members/{member_id}/credits.json'
        )
        if response.status_code >= 300:
            self._print_response(response)
            raise Exception('Request failed. See log.')
        else:
            try:
                return UserCreditsResponseSchema().load(response.json()['response'])
            except:
                print(json.dumps(response.json(), indent=2), file=sys.stderr)
                raise

    def update_credit(self, member_id: str, credit: Credit) -> None:
        response = self._session.put(
            f'{BASE_URL}/members/{member_id}/credits/{credit.id}.json',
            json=credit,
        )
        if response.status_code >= 300:
            self._print_response(response)
            raise Exception(f'Request failed (req body = {CreditSchema().dump(credit)}. See log.')

    def create_credit(self, member_id: str, event_id: str, amount: float, note: str) -> None:
        credit = {
            "amount": amount,
            "eventId": event_id,
            "note": note
        }
        response = self._session.post(
            f'{BASE_URL}/members/{member_id}/credits.json',
            json=credit,
        )
        if response.status_code >= 300:
            self._print_response(response)
            raise Exception(f'Request failed (req body = {json.dumps(credit)}. See log.')

    def delete_credit(self, member_id: str, credit: Credit):
        response = self._session.delete(f'{BASE_URL}/members/{member_id}/credits/{credit.id}.json')
        if 300 <= response.status_code and 404 != response.status_code:
            self._print_response(response)
            raise Exception(f'Request failed (req body = {CreditSchema().dump(credit)}. See log.')

    def get_paid_event_member_ids(self, event_id) -> list[str]:
        """
        Find all member IDs (not attendee IDs) that have paid for the given event
        """
        response = self._session.get(f'{BASE_URL}/events/{event_id}/attendees.json')
        if 300 <= response.status_code:
            self._print_response(response)
            raise Exception(f'Request failed. See log.')
        try:
            return [
                attendee['memberuri'].split('/')[-1]
                for attendee in response.json()['response']['attendees']
                if attendee['isPaid']
            ]
        except KeyError:
            self._print_response(response)
            raise

    @classmethod
    def _print_response(cls, response: requests.Response) -> None:
        response_body = response.content.decode('utf-8')
        print(f'Status = {response.status_code}', file=sys.stderr)
        print(f'Headers = {response.headers}', file=sys.stderr)
        content_type = response.headers["content-type"]
        print(f'Content Length ({content_type}) = {len(response_body)}', file=sys.stderr)
        print(json.dumps(response.json(), indent=2), file=sys.stderr)
