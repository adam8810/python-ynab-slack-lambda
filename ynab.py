import os
import json
import boto3
import requests

dynamo = boto3.client('dynamodb')

TABLE_NAME: str = 'ynab-slack-state'
YNAB_TOKEN: str = os.environ['YNAB_TOKEN']


def clean_obj(obj: dict) -> dict:
    """Converts a dynamodb dictionary into a dict that is easier to work with

    :param obj: Dynamodb dict
    :return: dict easier to work with
    """

    res = {}
    for key in obj.keys():
        res[key] = list(obj[key].values())[0]

    return res


class YNAB:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

        # Attempt to retrieve user state if it exists
        state = self.__get_state()

        if state is not None:
            self.state = state

    def __format(self, categories: dict) -> str:
        string = ''
        for group in categories:
            string += group + '\n'
            for category in categories[group]:
                string += '\t' + category + '\n'

        return string

    def __get_state(self) -> dict:
        """Retrieves state from dynamodb based on user_id

        TODO: Add error handling
        """
        result = dynamo.get_item(
            TableName=TABLE_NAME,
            Key={
                'user_id': {
                    'S': self.user_id
                }
            }
        )

        return clean_obj(result['Item'])

    def __get_categories(self) -> dict:
        """Retrieves ynab categories based on user budget_id
        """
        response = requests.get(
            'https://api.youneedabudget.com/v1/budgets/' +
            self.state['budget_id']+'/categories',
            headers={
                'Authorization': 'Bearer ' + YNAB_TOKEN
            }
        )

        # TODO: Add error handling
        return json.loads(response.content)['data']['category_groups']

    def search_categories(self, searchText: str) -> dict:
        """Returns formatted string of groups and categories within that match a given string

        :param searchText: String to compare categories to
        """
        groups = self.__get_categories()

        found = {}
        for group in groups:
            for group_category in group['categories']:
                if group_category['name'].lower().find(searchText.lower()) > -1:
                    # We create a new empty list if the key does not exist in `found`
                    if group['name'] not in found:
                        found[group['name']] = []

                    # Append category to found key
                    found[group['name']].append(group_category['name'])

        return self.__format(found)
