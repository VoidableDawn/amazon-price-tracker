import os
import smtplib

import requests
from bs4 import BeautifulSoup

"""
product_url = "https://www.amazon.com/gp/product/B0977FLLW3/
ref=ewc_pr_img_2?smid=AVY78AJDCWNYB&th=1"
"""
product_url = input("Paste the product url")
TARGET_PRICE = float(input("Enter the price you want to be notified if item price"
                           "drops below"))

# The headers will be specific to your browser and computer.
# Go to http://myhttpheader.com/ to view your browser headers.

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 "
                  "Safari/537.36,"
}
email = os.environ.get("EMAIl"),
password = os.environ.get("PASSWORD")
my_personal_email = os.environ.get("PERSONAL_EMAIL")

# Get webpage from http request

try:
    response = requests.get(url = product_url, headers = headers)
except (ConnectionError) as error:
    print(f"{error} type error occurred")
else:
    # If requests was successful, we can proceed to create BeautifulSoup
    # object from the markup file obtained from the request.
    response_text = response.text
    soup = BeautifulSoup(response_text, "html.parser")
    PRODUCT_NAME: str = soup.title.get_text()

    # Dig into soup object for price which is returned as a string and
    # convert to floating point number

    product_price: str = soup.find(name = "span", id = "price_inside_buybox").get_text()
    price = float(product_price.split("$")[1].replace(",", ""))
    print(price)

    # send email if price is lower than our Target Price
    if price < TARGET_PRICE:
        message = f"Subject: Amazon Price Alert!\n\n" \
                  f"Save ${round(TARGET_PRICE - price)}! \n" \
                  f"{PRODUCT_NAME} is on sale now for {product_price} only!\n" \
                  f"click the link below to buy now.\n\n" \
                  f"{product_url}"
        try:
            with smtplib.SMTP("smtp.mail.yahoo.com", ) as connection:
                connection.ehlo()
                connection.login(
                    user = email,
                    password = password
                )
                connection.sendmail(
                    from_addr = email,
                    to_addrs = my_personal_email,
                    msg = message
                )
                print("mail sent successfully!")
        except (smtplib.SMTPNotSupportedError, smtplib.SMTPException) as e:
            print(f"Mail not sent!\n {e}")
