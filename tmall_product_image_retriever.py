"""
This script is to retrive product images from Tmall
"""
#!/usr/bin/env python
#Coding:UTF8
#Python: >=3.6
try:
    import os
    import requests
    import re
except Exception as error:
    print("ERROR >>> Modules missing")
    print(error)
    os.system("pip install requests")
    print("INFO >>> Please run this script again")
    exit(-2)





def get_page_html(url, param=None):
    """
    To retrieve the page content
    """
    # To simulate the real website visiting
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
          'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'accept-encoding':'gzip, deflate, sdch'}
    try:
        print("\nGET >>> %s" % url)
        resp = None
        if param is None:
            resp = requests.get(url, headers=header)
        else:
            resp = requests.get(url, headers=header, params=param)

        if resp.status_code > 400:
            print("\nERROR >>> %d" % resp.status_code)
            return None
    except Exception as error:
        print("\nERROR >>> ")
        print(error)
        return None

    return resp.text


def save_product_image(url, location, num):
    """
    To retrieve product images
    """
    print("\nGET >>> %s" % url)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code >= 400:
            print("\nERROR >>> %d" % resp.status_code)

        binary_file = resp.content
        file_name = location + str(num) + ".jpg"
        f = open(file_name, 'wb')
        f.write(binary_file)
        f.close()

        print("\nSUCCESS >>> %s" % file_name)
    except Exception as error:
        print("\nERROR >>> ")
        print(error)





def get_product_images(url, location):
    """
    To retrieve the urls of product images
    """
    page_html = get_page_html(url)
    if len(page_html) <= 0:
        print("\nERROR >>> No content was returned for the URL: %s" % url)
        return

    image_urls = re.findall(re.compile(r'(//[^<>\'"]+?\.jpg)_[0-9]{2}x[0-9]{2}q[0-9]+\.jpg', re.RegexFlag.S|re.RegexFlag.I), page_html)
    if len(image_urls) <= 0:
        print("\nERROR >>> Can't find any product images")
        return

    for i in range(len(image_urls)):
        img_url = image_urls[i]
        if not img_url.startswith("http"):
            img_url = "http:" + img_url
        save_product_image(img_url, location, i)


print("""
        Tmall Product Image Retriever
""")

#Main entry
DEFAULT_ITEMS_FILE = "items.txt"
url_pool = []

items_file = input(
    "Please enter the file name containing item links (default: %s):" % DEFAULT_ITEMS_FILE)

if len(items_file) <= 2:
    items_file = DEFAULT_ITEMS_FILE

if not os.path.exists(items_file):
    print("\nERROR >>> File '%s' doesn't exist" % items_file)
    exit(0)

image_dir = os.path.abspath(os.path.dirname(items_file)) + "/images/"
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

with open(items_file) as file:
    url_pool = file.readlines()
    file.close()

while len(url_pool) > 0:
    item_url = url_pool.pop()
    item_id = re.findall(re.compile(r'id=([^=&]+)', re.RegexFlag.I), item_url)
    if len(item_id) <= 0:
        print("\nERROR >>> Can't find item id")
        continue

    item_image_dir = image_dir + item_id[0] + "/"
    if not os.path.exists(item_image_dir):
        os.mkdir(item_image_dir)

    get_product_images(item_url, item_image_dir)

print("\nSUCCESS >>> All finished")
