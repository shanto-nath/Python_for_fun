class Product:
  
  def __init__(self,name,price):
    self.name = name
    self.price = price

  def get_data(self):
    self.name = input("Enter name of the product: ")
    self.price = input("Enter price of the product: ")

  def put_data(self):
    print(self.name)
    print(self.price)


class DigitalProduct(Product):
  def __init__(self,link):
    self.link = link

  def get_link(self):
    self.link = input("Enter Product Link: ")

  def put_link(self):
    print(self.link)

ebook = DigitalProduct('')
ebook.get_data()
ebook.get_link()
ebook.put_data()
ebook.put_link()
