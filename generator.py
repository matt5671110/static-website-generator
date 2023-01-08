#!/usr/bin/env python3

import os, shutil, traceback
import markdown
from jinja2 import Environment, FileSystemLoader

class WebsiteGenerator:
	def __init__(self):
		self.abs_pwd = os.path.abspath(os.getcwd())
		print("Working Directory:",self.abs_pwd)
		self.env = Environment(loader=FileSystemLoader(os.path.join(self.abs_pwd, 'template')),
		 trim_blocks=True)
		self.site_data = {}
		self.post_data = {}
		self.default_metadata = {}
		self.getDefaultMetadata()
		self.processPostData()
		self.clearOutput()
		self.copyStaticAssets()
		self.renderContent()
		print("Done.")

	def getDefaultMetadata(self):
		with open(os.path.join(self.abs_pwd, 'default_metadata'), 'r') as defaultsfile:
			for line in defaultsfile:
				key, value = line.split(":")
				key = key.strip()
				value = value.strip()
				if key == "tags":
					value = value.split(" ")
				self.default_metadata[key] = value
			print("Default Metadata: {}".format(str(self.default_metadata)))

	def processPostData(self):
		post_files = os.listdir(os.path.join(self.abs_pwd, 'template', 'posts'))
		for filename in post_files:
			post_id = filename.rsplit(".", 1)[0]
			post_title = post_id.split("-")[3]
			post_date = post_id[:-len(post_title)-len("-")]
			path = os.path.join(self.abs_pwd, 'template', 'posts', filename)
			metadata_mark_count = 0
			post_metadata = {'title': post_title, 'date': post_date}
			post_markdown = None
			with open(path, 'r', encoding="utf-8") as post_file:
				for line in post_file:
					if line.strip() == "---" and metadata_mark_count < 2:
						metadata_mark_count += 1
						if metadata_mark_count == 2:
							break
						continue
					if metadata_mark_count == 1:
						key, value = line.split(":")
						key = key.strip()
						value = value.strip()
						if key == "tags":
							value = value.split(" ")
						post_metadata[key] = value
				post_markdown = str(post_file.read())
			post_metadata = {**self.default_metadata, **post_metadata}
			post_html = markdown.markdown(post_markdown)
			print("Process Post: {}".format(str(post_metadata)))
			self.post_data[post_id] = {**post_metadata, 'content': post_html, 'url': os.path.join('/posts',post_id + ".html")}

	def clearOutput(self):
		print("Clearing output directory ...")
		try:
			shutil.rmtree(os.path.join(self.abs_pwd, 'public'))
			os.mkdir(os.path.join(self.abs_pwd, 'public'))
			os.mkdir(os.path.join(self.abs_pwd, 'public', 'posts'))
		except:
			print("Error clearing output directory.")
			traceback.print_exc()

	def copyStaticAssets(self):
		print("Copying static assets to output directory ...")
		try:
			shutil.copytree(os.path.join(self.abs_pwd, 'template', 'static'), os.path.join(self.abs_pwd, 'public'), dirs_exist_ok=True)
		except:
			print("Error copying static assets.")
			traceback.print_exc()

	def renderContent(self):
		print("Determining pages to render ...")
		ignorelist = []
		with open(os.path.join(self.abs_pwd, 'ignore_pages'), 'r') as ignorefile:
			for line in ignorefile:
				ignorelist.append(line.strip())
		if len(ignorelist) != 0:
			print("Ignore:")
			for item in ignorelist:
				print("\t{}".format(item))
		page_templates = os.listdir(os.path.join(self.abs_pwd, 'template', 'pages'))
		page_templates = [item for item in page_templates if item not in ignorelist]
		print(str(page_templates))
		print("Rendering pages ...")
		for item in page_templates:
			print("\t{}".format(item))
			template = self.env.get_template(os.path.join('pages', item))
			template_html = template.render(self.site_data)
			with open(os.path.join(self.abs_pwd, 'public', item), 'w', encoding="utf-8") as file:
				file.write(template_html)

		print("Rendering posts ...")
		for post_id in self.post_data:
			print("\t{}".format(self.post_data[post_id]['title']))
			template = self.env.get_template(self.post_data[post_id]['template'])
			template_html = template.render({**self.site_data, 'post': {**self.post_data[post_id], 'id': post_id}})
			with open(os.path.join(self.abs_pwd, 'public', self.post_data[post_id]['url'][1:]), 'w', encoding="utf-8") as file:
				file.write(template_html)

if __name__ == '__main__':
	WebsiteGenerator()
