#!/usr/bin/env python3

import os, shutil, traceback
from datetime import datetime
import markdown
from jinja2 import Environment, FileSystemLoader

class WebsiteGenerator:
	def __init__(self):
		self.abs_pwd = os.path.abspath(os.getcwd())
		print("Working Directory:",self.abs_pwd)
		self.env = Environment(loader=FileSystemLoader(os.path.join(self.abs_pwd, 'template')),
		 trim_blocks=True)

	def generate(self):
		self.site_data = {}
		self.post_data = {}
		self.default_metadata = {}
		self.__getDefaultMetadata()
		self.__processPostData()
		self.__sortPostIdsByDate()
		self.__clearOutput()
		self.__copyStaticAssets()
		self.__renderContent()
		print("Done.")

	def __getDefaultMetadata(self):
		with open(os.path.join(self.abs_pwd, 'default_metadata'), 'r') as defaultsfile:
			for line in defaultsfile:
				key, value = line.split(":")
				key = key.strip()
				value = value.strip()
				if key == "tags":
					value = value.split(" ")
					value.sort()
				self.default_metadata[key] = value
			print("Default Metadata: {}".format(str(self.default_metadata)))

	def __processPostData(self):
		print("Processing posts ...")
		post_files = os.listdir(os.path.join(self.abs_pwd, 'template', 'posts'))
		for filename in post_files:
			if os.path.splitext(filename)[1] != ".md" and os.path.splitext(filename)[1] != ".html":
				print("Skipping {} because it is not a .md file.".format(filename))
				continue
			post_id = filename.rsplit(".", 1)[0]
			post_title = post_id.split("-", 3)[3]
			post_date = post_id[:-len(post_title)-len("-")]
			path = os.path.join(self.abs_pwd, 'template', 'posts', filename)
			metadata_mark_count = 0
			post_metadata = {'title': post_title, 'date': post_date}
			post_markdown = None
			with open(path, 'r', encoding="utf-8") as post_file:
				edit_data = []
				for line in post_file:
					if line.strip() == "---" and metadata_mark_count < 2:
						metadata_mark_count += 1
						if metadata_mark_count == 2:
							break
						continue
					if metadata_mark_count == 1:
						key, value = line.split(":", 1)
						key = key.strip()
						value = value.strip()
						if key == "tags":
							value = value.split(" ")
							value.sort()
						if key == "edited":
							edit_dates = value.split(" ")
							edit_dates.sort(reverse=True)
							for edit_date in edit_dates:
								edit_data.append({"date": edit_date, "reason": "None given."})
							continue
						if "-edit-reason" in key:
							date = key.removesuffix("-edit-reason")
							for edit in edit_data:
								if edit["date"] == date:
									edit["reason"] = value
							continue
						post_metadata[key] = value
				if edit_data:
					post_metadata["edited"] = edit_data
				post_markdown = str(post_file.read())
			post_metadata = {**self.default_metadata, **post_metadata}
			post_html = markdown.markdown(post_markdown, extensions=['fenced_code'], output_format = "html5")
			print("Process Post: {}".format(str(post_metadata)))
			self.post_data[post_id] = {**post_metadata, 'content': post_html, 'url': os.path.join('/posts',post_id + ".html")}

	def __sortPostIdsByDate(self):
		print("Sorting post ids by date ...")
		self.site_data['sorted_post_ids'] = sorted(self.post_data, key=lambda x:self.post_data[x]['date'], reverse=True)

	def __clearOutput(self):
		print("Clearing output directory ...")
		try:
			public_path = os.path.join(self.abs_pwd, 'public')
			if os.path.exists(public_path) and os.path.isdir(public_path):
				shutil.rmtree(public_path)
			os.mkdir(public_path)
			os.mkdir(os.path.join(public_path, 'posts'))
		except:
			print("Error clearing output directory.")
			traceback.print_exc()

	def __copyStaticAssets(self):
		print("Copying static assets to output directory ...")
		try:
			shutil.copytree(os.path.join(self.abs_pwd, 'template', 'static'), os.path.join(self.abs_pwd, 'public'), dirs_exist_ok=True)
		except:
			print("Error copying static assets.")
			traceback.print_exc()

	def __renderContent(self):
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
			template_html = template.render({'site': self.site_data, 'posts': self.post_data})
			with open(os.path.join(self.abs_pwd, 'public', item), 'w', encoding="utf-8") as file:
				file.write(template_html)

		print("Rendering posts ...")
		for post_id in self.post_data:
			print("\t{}".format(self.post_data[post_id]['title']))
			template = self.env.get_template(self.post_data[post_id]['template'])
			template_html = template.render({'site': self.site_data, 'post': {**self.post_data[post_id], 'id': post_id}})
			with open(os.path.join(self.abs_pwd, 'public', self.post_data[post_id]['url'][1:]), 'w', encoding="utf-8") as file:
				file.write(template_html)

if __name__ == '__main__':
	generator = WebsiteGenerator()
	generator.generate()
