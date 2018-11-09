# fa-grabber
anonymouse image grabber for few certain sites

Prerequisites:
1. launched tor or address of your other proxy server
2. mozilla browser
3. solved capchas at furaffinity and cookies
4. python with requests and beautifulsoup4 libraries. to get the libraries you have to launch following commands in your shell from administrator
    pip install requests[socks]
    pip install beautifulsoup4

Configuring this script:
1. write path to your download directory
2. write path to your cookies directory

Using this script:

You can just launch this file and it will grab images from the last page of your submissions or use certain link as an argument like this:
    ./grabber.py https://www.furaffinity.net/gallery/kacey
