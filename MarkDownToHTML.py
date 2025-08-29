import markdown
import sys
from bs4 import BeautifulSoup

ad_code = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7361580094970368"
     crossorigin="anonymous"></script>
"""

def insert_ad(soup, target_tag='head'):
	"""Inserts an ad code snippet after a specific tag.

	Args:
		soup: The BeautifulSoup object representing the HTML.
		target_tag: The tag after which to insert the ad.
	"""


def convert_markdown_with_ads(markdown_text):
	"""Converts Markdown to HTML and inserts ads.

	Args:
		markdown_text: The Markdown text to convert.

	Returns:
		The HTML string with inserted ads.
	"""

	html = '<html><head><link rel="stylesheet" href="css/modest.css"></head><body>' + markdown.markdown(markdown_text) + "</body></html>"
	soup = BeautifulSoup(html, 'html.parser')
	
	title_tag = soup.new_tag("title")
	title_tag.string = soup.html.body.h1.string
	soup.html.head.append(title_tag)
	consent_script = soup.new_tag("script")
	consent_script.string = """
		(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
		new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
		j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
		'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
		})(window,document,'script','dataLayer','GTM-W3PN4DNT');

	"""
	soup.html.head.insert(0, consent_script)
	
	print("Skipping CookieBot")
	
	#cookie_script = soup.new_tag("script")
	#cookie_script["id"] = "Cookiebot"
	#cookie_script["src"] = "https://consent.cookiebot.com/uc.js"
	#cookie_script["data-cbid"] = "8d09939f-268a-4e52-9740-41628a29fd31"
	#cookie_script["data-blockingmode"] = "auto"
	#cookie_script["type"] = "text/javascript"
	#soup.html.head.insert(0, cookie_script)
	
	tracking_tag = soup.new_tag("script")
	tracking_tag['async'] = None
	tracking_tag['src'] = "https://www.googletagmanager.com/gtag/js?id=G-02N74RKWVT"
	soup.html.head.append(tracking_tag)
	
	tracking_script = soup.new_tag("script")
	tracking_script.string = """
	  //window.dataLayer = window.dataLayer || [];
	  //function gtag(){dataLayer.push(arguments);}
	  gtag('js', new Date());

	  gtag('config', 'G-02N74RKWVT');
	"""
	soup.html.head.append(tracking_script)
	
	script_tag = soup.new_tag("script")
	script_tag['async'] = None
	script_tag['src'] = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7361580094970368"
	script_tag['crossorigin'] = "anonymous"
	soup.html.head.append(script_tag)
	
	noscript_tag = soup.new_tag("noscript")
	noscript_tag.string = """
		<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W3PN4DNT"
		height="0" width="0" style="display:none;visibility:hidden"></iframe>
	"""
	soup.html.body.insert(0, noscript_tag)
	
	return str(soup)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		html_filename = filename[:-2] + "html"
		print(f"Converting {filename} to {html_filename}")
		with open(html_filename, "w") as f:
			with open(filename, "r") as r:
				f.write("<!DOCTYPE html>\n")
				f.write(convert_markdown_with_ads(r.read()))