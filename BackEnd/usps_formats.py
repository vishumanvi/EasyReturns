from bs4 import BeautifulSoup

def getPriceCalculatorReq(packageDetails):
    zipSource = packageDetails['zipSource']
    zipDestination = packageDetails['zipDestination']
    ounces = packageDetails['ounces']

    file1 = open("xmls/priceCalulationRequest.xml", "r+")
    filebuf = file1.read()

    #print("file content is {}".format(filebuf))

    soup = BeautifulSoup(filebuf, 'xml')

    for tag in soup.find_all('ZipOrigination'):
        print(tag.get_text())
        tag.string.replace_with((str)(zipSource))
    
    for tag in soup.find_all('ZipDestination'):
        print(tag.get_text())
        tag.string.replace_with((str)(zipDestination))
    
    for tag in soup.find_all('Ounces'):
        print(tag.get_text())
        tag.string.replace_with((str)(ounces))

    return soup

    # zipSources = soup.find_all('ZipOrigination')
    # for zip in zipSources:
    #     print(zip.get_text())