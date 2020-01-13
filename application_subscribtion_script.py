import requests
import base64
import json
import params


def get_sub_content(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    sub_content = json.loads(response.content)
    return sub_content


def show_subs(url, headers):
    """
    Function shows all subscriptions in the tenant
        Parameters:
        url (str): takes url from the params.py
        Returns:
        List of strings with subscription id and details for each subscription
    """
    sub_content = get_sub_content(url, headers)
    print(sub_content)
    for x in range(len(sub_content['subscriptions'])):
        print((sub_content['subscriptions'])[x])


def show_subs_criteria(url, headers):
    """
    Function shows all subscriptions in the tenant
        Parameters:
        url (str): takes url from the params.py
        login (str): takes login from the params.py
        secret (str): takes secret from the params.py
        Returns:
        List of strings with subscription id of that subscriptions that have criteria defined
    """
    sub_content = get_sub_content(url, headers)
    c = 1
    if sub_content == '':
        print('Subscription is empty')
    else:
        print('\n\nSubscription list with criteria defined: ')
        for x in range(len(sub_content['subscriptions'])):
            subs_list = (sub_content['subscriptions'])[x]
            for i in subs_list:
                if i == "criteria":
                    print(subs_list['subscriptionId'])
                    c = c + 1
        if c <= 1:
            print('No criteria in subscriptions found !!!')


# def show_subs_resources(url, headers):
#     """
#     Function shows all subscriptions in the tenant
#         Parameters:
#         url (str): takes url from the subscription_operations.conf
#         login (str): takes login from the subscription_operations.conf
#         secret (str): takes secret from the subscription_operations.conf
#         Returns:
#         List of strings with subscription id of that subscriptions that have criteria defined
#     """
#     sub_content = get_sub_content(url, headers)
#     c = 1
#     if sub_content == '':
#         print('Subscription is empty')
#     else:
#         print('\n\nSubscription list with resources dio: ')
#         for x in range(len(sub_content['subscriptions'])):
#             subs_list = (sub_content['subscriptions'])[x]
#             for i in subs_list:
#                 if i == "criteria":
#                     print(subs_list['subscriptionId'])
#                     c = c + 1
#         if c <= 1:
#             print('No criteria in subscriptions found !!!')


def delete_subs_criteria(url, headers):
    """
    Function deletes all subscriptions with criteria defined
        Parameters:
        url (str): takes url from the params.py
        login (str): takes login from the params.py
        secret (str): takes secret from the params.py
        Returns:
        List of strings with subscription id of that subscriptions that have criteria defined and deleted
    """
    sub_content = get_sub_content(url, headers)

    for x in range(len(sub_content['subscriptions'])):
        subs_list = (sub_content['subscriptions'])[x]
        for i in subs_list:
            if i == "criteria":
                print(subs_list['subscriptionId'])
                url = (platform_url + '/' + subs_list['subscriptionId'] + '')
                print(url)
                delete = requests.delete(url, headers=headers)
                print('Server response {}'.format(delete.content))


 def delete_all_subs(url, headers):
     """
     Function deletes all subscriptions
         Parameters:
         url (str): takes url from the params.py
         login (str): takes login from the params.py
         secret (str): takes secret from the params.py
         Returns:
         List of strings with subscription id of that subscriptions that was deleted
     """
     sub_content = get_sub_content(url, headers)
     print(sub_content)
     delete = requests.delete(url, headers=headers)
     print('Server response {}'.format(delete.content))


def main():
    print("\nThis script can show all subscriptions in tenant, \n"
          "Show subscriptions that have any criteria defined, \n"
          "Delete all subscriptions with any criteria defined or \n"
          "Delete all subscriptions\n")

    while True:
        print("\nMake a choice\n"
              "1. To show all subscriptions in tenant which admin is defined in params file\n"
              "2. To show all subscriptions in tenant with criteria which admin is defined in params file\n"
              "80. To DELETE all subscriptions in tenant with criteria which admin is defined in params file\n"
              "99. To DELETE all subscriptions in tenant which admin is defined in params file\n"
              "0. To exit from a program\n")
        choice = input('Waiting for your choice > ')
        if choice == '1':
            show_subs(user_url, user_headers)
        elif choice == '2':
            show_subs_criteria(user_url, user_headers)
        elif choice == '80':
            delete_subs_criteria(user_url, user_headers)
        elif choice == '99':
            delete_all_subs(platform_url, user_headers)
        elif choice == '0':
            print('Exiting...')
            exit()
        else:
            print('Function not found')


ip_port = params.ip_port
platform_url = ip_port + '/m2m/subscriptions'
user_url = platform_url + '?type=resources'
login = params.login
secret = params.secret
login_pass = login + ':' + secret
user_auth64 = base64.b64encode(login_pass.encode()).decode()
user_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': 'Basic %s' % user_auth64}

if __name__ == '__main__':
    main()
