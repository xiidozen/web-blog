import json
import os
import time
import numpy as np
import config
import sys
import random
import re
import google.generativeai as genai

# File to store blog topics and subtopics
TOPICS_FILE = 'blog_topics.json'

def call_openai_api(prompt, model="gemini-1.5-flash",):
	"""Execute the given prompt with retries if rate limit or unknown errors occur."""
	prmpt = "\n".join([x["content"] for x in prompt])

	genai.configure(api_key=config.API_KEY)

	model = genai.GenerativeModel(model)
	#print(prmpt)
	response = model.generate_content(prmpt)
	while not hasattr(response, "text"):
		print("Response had no text, retrying...")
		response = model.generate_content(prmpt)
	text = response.text.replace("\\n", "\n").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2013', '-').replace('\u2014', '-').replace('\u012b', '1').replace('\u2026', '...')
	if(text[0:7] == "```json"):
		text = text[7:]
	if(text[-3:] == "```"):
		text = text[:-3]
	text = text.strip()

	return text


def generate_idea(prompt):
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": prompt + "  Send the reply as plain text with proper spacing"}
	]
	
	idea = call_openai_api(messages)
	idea = ' '.join(re.findall('[A-Z][a-z]*', idea)).strip()
	while not " " in idea:
		print(idea + " had no spaces, retrying...", flush=True)
		idea = call_openai_api(messages)
	idea = idea.replace('"','').replace("'","")
	return idea

def generate_outline(topic):
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": f"Generate a detailed outline in JSON format for a blog post on the topic: '{topic}'." + " The JSON should include a list of sections, with each section having a 'title' and a 'description'. Format it in this way: {[{\"title\":\"The title\", \"description\":\"The description\"}]}  The description should be simple sentences with no formatting or structure.  Include only the requested json, and no other data or formatting.  Reply in plain text with no special characters."}
	]
	outline_json = call_openai_api(messages)
	#print(outline_json)
	#sys.stdout.flush()
	try:
		return json.loads(outline_json)
	except json.JSONDecodeError:
		print("Failed to decode JSON response for outline.")
		sys.stdout.flush()
		return None

def generate_section(topic, section_title, section_description):
	print(section_title)
	sys.stdout.flush()
	messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": f"Write a detailed section in markdown format for a blog post on the topic: '{topic}' with the section title: '{section_title}'. The section should cover the following description: {section_description}.  Make the section at least 600 words long, more is better."}
	]
	return call_openai_api(messages)

def load_topics():
	if os.path.exists(TOPICS_FILE):
		with open(TOPICS_FILE, 'r') as f:
			return json.load(f)
	return []

def save_topic(topic, subtopic=None):
	topics = load_topics()
	if subtopic:
		for t in topics:
			if t['topic'] == topic:
				t['subtopics'].append(subtopic)
				break
	else:
		topics.append({'topic': topic, 'subtopics': []})
	with open(TOPICS_FILE, 'w') as f:
		json.dump(topics, f, indent=4)

def get_next_topic():
	topics = load_topics()
	if topics:
		most_recent_topic = topics[-1]
		num_subtopics = len(most_recent_topic['subtopics'])
		gaussian_choice = np.random.normal(loc=4, scale=1)
		if num_subtopics < gaussian_choice:
			subtopics = most_recent_topic['subtopics']
			subtopic_prompt = f"Generate a subtopic that is related to the main topic '{most_recent_topic['topic']}'.  Provide me only the title of the idea with no additional information or formatting.  Only include alphanumeric characters and no special characters."
			if subtopics:
				subtopic_prompt += f"  Avoid the following subtopics: {', '.join(subtopics)}."
			subtopic = generate_idea(subtopic_prompt)
			return most_recent_topic['topic'], subtopic

	# Get all main topics to avoid duplicates
	main_topics = [t['topic'] for t in topics]
	main_topic_prompt = f"Generate an interesting blog post idea.  Provide me only the title of the idea with no additional information or formatting."
	if main_topics:
		main_topic_prompt += f"  Avoid the following topics: {', '.join(main_topics)}."
	return generate_idea(main_topic_prompt), None

def main():
	main_topic, subtopic = get_next_topic()

	if subtopic:
		post_topic = f"{main_topic} - {subtopic}"
	else:
		post_topic = main_topic
	#post_topic = post_topic.replace('"','').replace("'","")
	print(post_topic)
	sys.stdout.flush()

	outline = generate_outline(post_topic)

	if outline:
		blog_post_content = []

		for section in outline:
			section_title = section['title']
			section_description = section['description']
			section_content = generate_section(post_topic, section_title, section_description)
			if section_content:
				blog_post_content.append(f"{section_content}")

		blog_post = '\n\n'.join(blog_post_content)

		post_content = f"""

# {post_topic}
---

*Disclaimer: This blog post was written by an AI.*

---

{blog_post}

---

*Disclaimer: This blog post was written by an AI.*
"""

		# Save the topic and subtopic
		save_topic(main_topic, subtopic)

		# Save the blog post to a file
		post_filename = f"{post_topic.replace(' ', '_').replace(':', '_')}.md"
		with open(post_filename, 'w', errors='ignore') as f:
			f.write(post_content)

		print(f"Blog post '{post_topic}' has been generated \nand saved as {post_filename}")
		sys.stdout.flush()
		return post_filename
	else:
		print("Failed to generate the blog post outline.")
		sys.stdout.flush()
	return None

if __name__ == "__main__":
	main()
