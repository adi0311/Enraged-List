from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
from . import models

BASE_CRAIGLIST_URL = 'https://delhi.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
	return render(request, 'base.html')


def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
	# print(final_url)
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')
	post_listings = soup.find_all('li', {'class': 'result-row'})
	# print(post_listings)
	# post_title = post_listings[0].find(class_='result-title').text
	# post_url = post_listings[0].find('a').get('href')
	# post_price = post_listings[0].find(class_='result-price')
	# print(post_title)
	# print(post_url)
	# print(post_price)
	final_postings = []
	for post in post_listings:
		if post.find(class_='result-image').get('data-ids'):
			post_image_id = post.find('a').get('data-ids')
			if ',' in post_image_id:
				# We only need first id to display the first image
				index =  post_image_id.index(',')
				# Chopping off the "1:" portion
				post_image_id = post_image_id[2:index]
			else:
				post_image_id = post_image_id[2:]
			post_image = BASE_IMAGE_URL.format(post_image_id)
		else:
			post_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSZfbLkSFvDXC1kAe-aNkByig7gFx3ASYkIcflU0BVog3kNhw6N&usqp=CAU"
		print(post_image)
		post_title = post.find(class_='result-title').text
		post_url = post.find('a').get('href')
		price_finder = post.find(class_='result-price')
		if not price_finder:
			post_price = "N/A"
		else:
			post_price = price_finder.text
		final_postings.append((post_title, post_url, post_price, post_image))

	context = {
		'search': search,
		'final_postings': final_postings,
	}
	return render(request, 'my_app/new_search.html', context)
