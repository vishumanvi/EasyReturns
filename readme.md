## Inspiration
Online e-commerce has now surpassed retail purchases in the US and will continue to dominate in the future. While it has become extremely convenient and quick to get online orders delivered to home, there is still a lot to be desired for shipping packages or returns from home. Most online orders don't provide a return shipping label. Customers currently have an option to pay and print return label online but this adds a dependency on having a printer at home. They then have to schedule a package pickup which is not always an option especially in apartments/gated communities and adds security concerns not to mention pickup schedule might not work well for all customers. This leaves most customers heading to a post office. We think sending packages/returns from home should be as easy as receiving them. Welcome to our app, EasyReturns. EasyReturns provides a seamless way to send packages from home.

## What it does
EasyReturns simplifies sending and returning packages from home, providing a more secure and convenient way to customers. The end to end app workflow is as follows.

1. Customer login to EasyReturns app.
2. Customer enters sender and recipient address (can be enhanced by taking a picture of original shipping label and auto-populating addresses and swapping them) 
3. App shows prices for various shipping options (First class, Priority, etc) using USPS APIs.
4. Customer makes the payment using Credit Card/Paypal/Apple Pay.
5. On successful payment, app generates a QR code and a unique number.
6. Customer can either print it or write down just the number on a paper and stick it to the package.
7. Customer then schedules a package pickup. In case of apartments/gated communities that have a locker facility, app provides an option to generate a passcode for one of the available locker that customer can place the package in. (Future enhancement)
8. Customer places the package in the locker.
9. USPS Postman gets notified about the pickup with locker details. Else, pickup from home (current process) 
10. USPS Postman scans the barcode/QR code/unique number on the package to verify if it's valid and paid for and automatically gets sender and receiver details required to ship it.

This way, no sender/receiver sensitive PII data is ever printed on a shipping label and therefore more secure.

## How we built it
Technologies: 
Front end: HTML 5, CSS 3, Javascript
Backend : Python, Flask, PickleDB, BeautifulSoup
External: USPS APIs (https://www.usps.com/business/web-tools-apis/documentation-updates.htm)

## Challenges we ran into
1. Understanding and parsing USPS APIs XML request/responses.
2. Integrating front end and back end.
3. Time constraints in completing the hackathon. 

## Accomplishments that we're proud of
1. Integrated with production USPS APIs.
2. Created a working software in few hours.
3. Design that supports both mobile and web app.
4. We applied agile methodologies for managing work.


## What we learned
1. Integration issues.
2. Time management.

## What's next for EasyReturns
1. Enhancements for smart locker feature.
2. Integration with USPS pickup service.

