import os, shutil
from jinja2 import Environment, FileSystemLoader

class WebsiteGenerator:
	def __init__(self):
		self.abs_pwd = os.path.abspath(os.getcwd())
		print("Working Directory:",self.abs_pwd)
		self.env = Environment(loader=FileSystemLoader(os.path.join(self.abs_pwd, 'template')),
		 trim_blocks=True)


if __name__ == '__main__':
	WebsiteGenerator()
