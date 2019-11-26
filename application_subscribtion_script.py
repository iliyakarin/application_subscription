import requests
import base64
import json
import params


def show_subs(url, headers):
    """
    Function shows all subscriptions in the tenant with criteria defined

        Parameters:
        url (str): takes url from the subscription_operations.conf

        Returns:
        List of strings with subscription id and details for each subscription
    """
    response = requests.get(url, headers=headers)
    sub_content = json.loads(response.content)
    if response.status_code == 404:
        print(headers)
        print(url)
        print('Server response {}'.format(response.content))
    else:
        for x in range(len(sub_content['subscriptions'])):
            print((sub_content['subscriptions'])[x])


def show_subs_criteria(url, headers):
    """
    Function shows all subscriptions in the tenant

        Parameters:
        url (str): takes url from the subscription_operations.conf
        login (str): takes login from the subscription_operations.conf
        secret (str): takes secret from the subscription_operations.conf

        Returns:
        List of strings with subscription id of that subscriptions that have criteria defined
    """
    response = requests.get(url, headers=headers)
    sub_content = json.loads(response.content)
    if response.status_code == 404:
        print(headers)
        print(url)
        print('Server response {}'.format(response.content))
    else:
        if sub_content == '':
            print('Subscription is empty')              # Not sure if working
        else:
            for x in range(len(sub_content['subscriptions'])):
                subs_list = (sub_content['subscriptions'])[x]
                for i in subs_list:
                    if i == "criteria":
                        print(subs_list['subscriptionId'])
                    else:
                        print('No criteria in subscription found')      # Not sure if working


def delete_subs_criteria(url, headers):
    """
    Function deletes all subscriptions with criteria defined

        Parameters:
        url (str): takes url from the subscription_operations.conf
        login (str): takes login from the subscription_operations.conf
        secret (str): takes secret from the subscription_operations.conf

        Returns:
        List of strings with subscription id of that subscriptions that have criteria defined and deleted
    """
    response = requests.get(url, headers=headers)
    sub_content = json.loads(response.content)
    if response.status_code == 404:
        print(headers)
        print(url)
        print('Server response {}'.format(response.content))
    else:
        for x in range(len(sub_content['subscriptions'])):
            subs_list = (sub_content['subscriptions'])[x]
            for i in subs_list:
                if i == "criteria":
                    print(subs_list['subscriptionId'])
                    url = (platform_url + '/' + subs_list['subscriptionId'] + '')
                    print(url)
                    delete = requests.delete(url, headers=headers)
                    print('Server response {}'.format(delete.content))


def main():
    print("\nThis script can show all subscriptions in tenant, \n"
          "Show subscriptions that have any criteria defined or \n"
          "Delete all subscriptions with any criteria defined\n")

    while True:
        print("\nMake a choice\n"
              "1. To show all subscriptions in tenant which admin is defined in params file\n"
              "2. To show all subscriptions in tenant with criteria which admin is defined in params file\n"
              "8. To DELETE all subscriptions in tenant with criteria which admin is defined in params file\n"
              "0. To exit from a program\n")
        choice = input('Waiting for your choice > ')
        if choice == '1':
            show_subs(user_url, user_headers)
        elif choice == '2':
            show_subs_criteria(user_url, user_headers)
        elif choice == '8':
            delete_subs_criteria(user_url, user_headers)
        elif choice == '0':
            print('Exiting...')
            exit()
        else:
            print('Function not found')


ip_port = params.ip_port
platform_url = 'http://' + ip_port + '/m2m/subscriptions'
user_url = platform_url + '?type=resources'
login = params.login
secret = params.secret
login_pass = login + ':' + secret
user_auth64 = base64.b64encode(login_pass.encode()).decode()
user_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': 'Basic %s' % user_auth64}

if __name__ == '__main__':
    main()
