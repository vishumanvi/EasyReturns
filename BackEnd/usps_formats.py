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
        #print(tag.get_text())
        tag.string.replace_with((str)(zipSource))

    for tag in soup.find_all('ZipDestination'):
        #print(tag.get_text())
        tag.string.replace_with((str)(zipDestination))

    for tag in soup.find_all('Ounces'):
        #print(tag.get_text())
        tag.string.replace_with((str)(ounces))

    return soup


def getPriceResponse(reqXml):
    soup = BeautifulSoup(reqXml, 'xml')
    res = []
    for package in soup.find_all('Postage'):
        #if package['CLASSID'] == "0":
            # for service in package.find_all('SpecialService'):
            #     serviceName = service.find('ServiceName').get_text()
            #     price = service.find('Price').get_text()
            #     res.append({'ServiceType': serviceName, 'Price': price})
        serviceName = package.find('MailService').get_text()
        serviceName = serviceName.split('&')[0]
        price = package.find('Rate').get_text()
        res.append({'ServiceType': serviceName, 'Price': price})
    return res
