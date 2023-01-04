import os, shutil, traceback
from jinja2 import Environment, FileSystemLoader

class WebsiteGenerator:
	def __init__(self):
		self.abs_pwd = os.path.abspath(os.getcwd())
		print("Working Directory:",self.abs_pwd)
		self.env = Environment(loader=FileSystemLoader(os.path.join(self.abs_pwd, 'template')),
		 trim_blocks=True)
		self.clearOutput()
		self.copyStaticAssets()
		self.renderContent()
		print("Done.")

	def clearOutput(self):
		print("Clearing output directory ...")
		try:
			shutil.rmtree(os.path.join(self.abs_pwd, 'public'))
			os.mkdir(os.path.join(self.abs_pwd, 'public'))
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
		content_templates = os.listdir(os.path.join(self.abs_pwd, 'template', 'content'))
		content_templates = [item for item in content_templates if item not in ignorelist]
		print(str(content_templates))
		print("Rendering content ...")
		for item in content_templates:
			print("\t{}".format(item))
			template = self.env.get_template(os.path.join('content', item))
			template_html = template.render()
			with open(os.path.join(self.abs_pwd, 'public', item), 'w') as file:
				file.write(template_html)

if __name__ == '__main__':
	WebsiteGenerator()
