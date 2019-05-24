#!/usr/bin/python
##
# CLI script to retrieving data from SLACK
##
import requests
import argparse
import sys
import pandas as pd
from decimal import *
from tabulate import tabulate


class SlackUsers:

    url = ''
    token = ''

    @staticmethod
    def get_arg_parser():
        parser = argparse.ArgumentParser(
            description='Get users list from slack who are all not having their profile pictures'
        )
        parser.add_argument('-slackToken', '--token', help='Slack Token')

        return parser

    def call_api(self):
        self.url = 'https://slack.com/api/users.list?token='+self.token+'&limit=1000&pretty=1'
        session_with_header = requests.Session()
        session_with_header.headers.update({'Authorization': 'Basic '+self.token})
        response = session_with_header.get(self.url)

        if response.status_code == 200:
            return response.json()
        else:
            print("API Failure")
            sys.exit(1)

    def get_users(self):
        response_object = self.call_api()
        user_dict = {}
        sorted_user_dict = {}
        user_loop_counter = 1
        sorted_loop_counter = 1
        for profile in response_object['members']:
           if ('email' in profile['profile'] and profile['deleted'] == False and 'image_original' not in profile['profile']):
            name = profile['profile']['real_name'].lower()
            email = profile['profile']['email'].lower()
            user_dict[user_loop_counter] = {"name":name,"email":email}
            user_loop_counter+= 1

        for key in sorted(user_dict.values()):
            sorted_user_dict[sorted_loop_counter] = {"display_name":key['name'],"email":key['email']}
            sorted_loop_counter+= 1


        data_table = pd.DataFrame(sorted_user_dict)
        data_table = data_table.T
        data_table.columns = ["Name", "Email"]
        print(tabulate(data_table, headers="keys", tablefmt="psql"))
    
    def run(self):
        parser = self.get_arg_parser()
        arguments = parser.parse_args()
        if not all([arguments.token]):
            parser.print_help()
            sys.exit(1)
        else:
            self.token = arguments.token
            self.get_users()


if __name__ == '__main__':
    b = SlackUsers()
    b.run()