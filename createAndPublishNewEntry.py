import GenerateBlogPost as genPost
import MarkDownToHTML as md2html
import genIndex
from google.cloud import storage

def main():
	storage_client = storage.Client()

	blogFile = genPost.main()

	html_filename = blogFile[:-2] + "html"
	with open(html_filename, "w") as f:
		with open(blogFile, "r") as r:
			f.write(md2html.convert_markdown_with_ads(r.read()))

	genIndex.main("blog_topics.json")


	bucket = storage_client.bucket("blog-web-data")
	blob = bucket.blob(html_filename)
	blob.upload_from_filename(html_filename)
	blob = bucket.blob("index.html")
	blob.upload_from_filename("index.html")

if __name__ == "__main__":
	main()