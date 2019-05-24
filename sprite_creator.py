from PIL import Image
import math, os

class Sprite(object):
	def __init__(self, width, height, across, gap, name):
		self.item_width = width
		self.item_height = height
		self.items_across = across
		self.gap = gap
		self.sheet_width = self.item_width * self.items_across + self.gap * (self.items_across - 1)
		self.sheet_height = self.item_height # this will be increased as we add more images
		self.filename = name + '.png'
		self.sheet = None
		
		self.current_location = 0
		self.current_col = 0
		self.current_row = 0
		self.current_x = 0
		self.current_y = 0
	
	def open_from_file(self, location=None):
		if location:
			self.current_location = location
		if not os.path.isfile(self.filename):
			self.create_new()
		else:
			self.sheet = Image.open(self.filename)
		
	def create_new(self):
		self.sheet = Image.new('RGBA', (self.sheet_width, self.sheet_height))
	
	def add_next_image_from_file(self, image_path):
		image = Image.open(image_path)
		self.add_next_image(image)
	
	def add_next_image(self, img):
		self.increment_current_location() # adding the default image will be handled separately
		if self.current_col == 0:
			old_sheet = self.sheet
			self.sheet_height = self.sheet_height + self.gap + self.item_height
			self.create_new()
			self.sheet.paste(old_sheet, (0,0))
		box = (self.current_x, self.current_y)
		img = img.resize((self.item_width, self.item_height), Image.ANTIALIAS)
		self.sheet.paste(img, box)
	
	def increment_current_location(self):
		self.update_current_location(self.current_location + 1)
	
	def update_current_location(self, new_location):
		self.current_location = new_location
		self.current_col = self.current_location % self.items_across
		self.current_row = math.floor(self.current_location / self.items_across)
		self.current_x = self.current_col * (self.item_width + self.gap)
		self.current_y = self.current_row * (self.item_height + self.gap)
	
	def get_slice(self, location):
		self.update_current_location(location)
		crop_rectangle = (self.current_x, self.current_y, self.current_x + self.item_width, self.current_y + self.item_height)
		return self.sheet.crop(crop_rectangle)
	
	def save(self):
		self.sheet.save(self.filename)