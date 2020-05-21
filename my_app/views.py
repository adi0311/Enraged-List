from django.shortcuts import render, get_object_or_404
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
from .models import Search, VisitedArticle

BASE_CRAIGLIST_URL = 'https://delhi.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
	return render(request, 'base.html')


def new_search(request):
	search = request.POST.get('search')
	if search:
		Search.objects.create(search=search)
		final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
		response = requests.get(final_url)
		data = response.text
		soup = BeautifulSoup(data, features='html.parser')
		post_listings = soup.find_all('li', {'class': 'result-row'})
		final_postings = []
		for post in post_listings:
			if post.find(class_='result-image').get('data-ids'):
				post_image_id = post.find('a').get('data-ids')
				if ',' in post_image_id:
					index =  post_image_id.index(',')
					post_image_id = post_image_id[2:index]
				else:
					post_image_id = post_image_id[2:]
				post_image = BASE_IMAGE_URL.format(post_image_id)
			else:
				post_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSZfbLkSFvDXC1kAe-aNkByig7gFx3ASYkIcflU0BVog3kNhw6N&usqp=CAU"
			# print(post_image)
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
	else:
		return render(request, 'base.html', {'error_message': "Attention: You need to enter what you are looking for!!!",})


def article_detail_view(request):
	article_url = request.POST.get('article_url')
	article_image_url = request.POST.get('article_image')
	response = requests.get(article_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')
	post_title = soup.find_all('span', {'id': 'titletextonly'})
	post_content = soup.find_all('section', {'id': "postingbody"})
	for title in post_title:
		post_title = title.text
		break
	for content in post_content:
		post_description = content.text
	web_index = post_description.find('http')
	add_index = post_description.find('.com/')
	phone_index = post_description.find('Tel:')
	if web_index != -1 and add_index != -1:
		web_url = post_description[web_index: add_index+5]
	else:
		web_url = "N/A"
	if add_index != -1 and phone_index != -1:
		address = post_description[add_index+5: phone_index]
	else:
		address = "N/A"
	if phone_index != -1:
		contact = post_description[phone_index:]
	else:
		contact = "N/A"
	if web_index != -1:
		post_description = post_description[:web_index]+"."
	else:
		post_description = "N/A"
	print(article_url)
	print(article_image_url)
	VisitedArticle.objects.create(article_title=post_title, article_url=article_url)
	context = {
		'post_title': post_title,
		'post_image': article_image_url,
		'post_description': post_description[29:],
		'web_url': web_url,
		'address': address,
		'contact': contact[5:],
	}
	return render(request, 'my_app/article.html', context)

