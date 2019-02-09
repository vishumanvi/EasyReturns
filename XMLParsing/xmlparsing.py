from bs4 import BeautifulSoup
file1 = open("response.xml","r+")
filebuf = file1.read()

print("file content is {}".format(filebuf))

soup = BeautifulSoup(filebuf,'xml')

prices = soup.find_all('Rate')
for price in prices:
    print(price.get_text())

