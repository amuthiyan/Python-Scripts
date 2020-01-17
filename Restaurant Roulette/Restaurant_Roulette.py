
# coding: utf-8

# # Restaurant Roulette Development

# Restaurant roulette will be a service whereby friends can easily choose a restaurant to go to together. Simply enter categories that are completely out, eg. someone definitly doesn't want Chinese food. Then choose priority, price, ratings, or both. And hit enter. Restaurant Roulette will pull from the Zomato API: `https://developers.zomato.com/api` and give one recommendation out of the list. No arguing, no decision paralysis. If the choice is absolutely not acceptable, it can be respun until an acceptable option is found. This reduces the "Lets check out all the options" mentality by only presenting one definitive option at a time.

# First step, gathering a list of the restaurants in the city:

# In[1]:

import requests
from pprint import pprint
import json
import random


# In[2]:

ACCESS_CODE = '643b43fb68f836827565f9c0fe4006c5'


# In[3]:

'''
Takes as input the API user code and the name of the city, and returns a list of all the restaurants in the city
'''
def getAllRestaurants(city_name,ACCESS_CODE):
    city_url = "https://developers.zomato.com/api/v2.1/cities?q=" + city_name
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ACCESS_CODE}

    #Get code of city
    response = requests.get(city_url, headers=header).json()
    city_code = str(response['location_suggestions'][0]['id'])
    
    #Get Restaurants in that city
    
    restaurants_list = []
    for start_num in range(20,101,20):
        restaurant_url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + city_code + '&entity_type=city&count=20&start='+str(start_num)
        response = requests.get(restaurant_url, headers=header).json()
        restaurants_dict = response['restaurants']
        for restaurant_num in range(len(restaurants_dict)):
            restaurants_list.append(restaurants_dict[restaurant_num]['restaurant']['name'])
            

    return restaurants_list


# In[4]:

'''
Takes as input the API user code and the name of the city, and returns a dictionary of restaurants sorted by cuisine.
'''
def getRestaurantByCuisine(city_name,ACCESS_CODE):
    city_url = "https://developers.zomato.com/api/v2.1/cities?q=" + city_name
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ACCESS_CODE}

    #Get code of city
    response = requests.get(city_url, headers=header).json()
    city_code = str(response['location_suggestions'][0]['id'])
    
    #Get Restaurants by cuisine in that city
    cuisine_dict = {}
    for start_num in range(20,101,20):
        restaurant_url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + city_code + '&entity_type=city&count=20&start='+str(start_num)
        response = requests.get(restaurant_url, headers=header).json()
        restaurants_dict = response['restaurants']
        for restaurant_num in range(len(restaurants_dict)):
            cuisines_string = restaurants_dict[restaurant_num]['restaurant']['cuisines']
            cuisines_list = cuisines_string.strip('()').split(', ')
            #print(cuisines_list)
            for cuisine in cuisines_list:
                if cuisine not in cuisine_dict:
                    cuisine_dict[cuisine] = []
                cuisine_dict[cuisine].append(restaurants_dict[restaurant_num]['restaurant']['name'])
    return cuisine_dict


# In[5]:

'''
Takes as input the restaurant by cuisine, and begins the process of suggesting a restaurant
'''
def giveSuggestion(restaurant_by_cuisine_dict,bad_list):
    for cuisine in bad_list:
         restaurant_by_cuisine_dict.pop(cuisine, None)
    restaurant_list = []
    for cuisine in restaurant_by_cuisine_dict:
        restaurant_list = list(set(restaurant_list + restaurant_by_cuisine_dict[cuisine]))
    return random.choice(restaurant_list)


# In[7]:

#Main Driver

print("Lets choose a restaurant!")
city_name = input('What city are you in?')
num_peeps = int(input("How many of you are there? Everyone gets a veto!"))
print('Everyone gets to veto a specific cuising. Type your veto below: ')
bad_list = []
for i in range(num_peeps):
    bad_list.append(input('Veto '+str(i+1)+': '))
while(True):
    print('Generating choice...')
    restaurant_by_cuisine_dict = getRestaurantByCuisine(city_name,ACCESS_CODE)
    choice = giveSuggestion(restaurant_by_cuisine_dict,bad_list)
    print('We suggest you go to '+choice)
    go_again = input('Want to roll again?(y/n)')
    if go_again == 'n':
        break
print('Hope you like the restaurant!')


# In[ ]:



