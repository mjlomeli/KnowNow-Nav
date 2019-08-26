from bs4 import BeautifulSoup
import urllib3, certifi
from requests_html import HTMLSession


keywords = ["cancer", "treatment", "radiotherapy"]

# urls = ["https://www.cancerresearchuk.org/about-cancer/cancer-chat/thread/radiotherapy-side-effects", "https://www.reddit.com/r/cancer/comments/522471/what_is_radiation_therapy_like/"]



class Scraper():
	def __init__(self):
		self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

		query_url = self.site_lookup(["radiotherapy", "treatment"], "reddit.com/r/cancer") #reddit query works
		# query_url = self.site_lookup(["radiotherapy", "treatment"], "cancerresearchuk")  #cancerresearchuk does not
		print(query_url)

		search_results = self.get_search_urls(query_url)
		print(search_results)

		keyword_posts = self.grab_posts(keywords, search_results)
		print(keyword_posts)

	def site_lookup(self, query, site):
		if "cancerresearchuk" in site:
			url = "https://find.cancerresearchuk.org/?xss-q=" + query.pop()
			for item in query:
				url = url + "+" + item
			return url
		elif "reddit.com/r/cancer" in site:
			url = "https://www.reddit.com/r/cancer/search/?q=" + query.pop()
			for item in query:
				url = url + "%20" + item
			return url + "&restrict_sr=1"

	def get_search_urls(self, query_url):
		search_results = []

		if "cancerresearchuk" in query_url:
			tag_filter = "a"
			id_type = "class"
			id_filter = "cr-search-result__link"
		elif "reddit.com/r/cancer" in query_url:
			tag_filter = "a"
			id_type = "data-click-id"
			id_filter = "body"

		session = HTMLSession()
		resp = session.get(query_url)
		resp.html.render()

		soup = BeautifulSoup(resp.html.html, "lxml")

		links = soup.find_all(tag_filter, {id_type:id_filter})

		for link in links:
			search_results.append(link.get('href'))

		if "reddit" in query_url:
			new_results = []
			for item in search_results:
				item = "https://www.reddit.com" + item
				new_results.append(item)
			search_results = new_results

		return search_results


	def grab_posts(self, keywords, urls):

		formatting_cuts = ["\xa0"]

		all_paras = []

		for url in urls:

			if "cancerresearchuk" in url:
				tag_filter = "div"
				id_type = "class"
				id_filter = "post-content-inner"
			elif "reddit" in url:
				tag_filter = "div"
				id_type = "data-test-id"
				id_filter = "comment"

			response = self.http.request('GET', url)

			soup = BeautifulSoup(response.data, "lxml")

			posts = soup.find_all(tag_filter, {id_type:id_filter})

			for post in posts:
				paras = post.find_all('p')

				keyword_found = False
				para_string = []

				for p in paras:
					if p.string is not None:
						if p.string not in formatting_cuts:
							para_string.append(p.string.replace(u'\xa0',' '))
							for keyword in keywords:
								if keyword in p.string:
									keyword_found = True
									break

				if keyword_found:
					all_paras.append(para_string)

		return all_paras

s = Scraper()

