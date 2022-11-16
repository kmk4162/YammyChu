import os
import sys
import urllib.request
from django.shortcuts import render


def news():
    client_id = "q3xdnYmqL_0__IhS5dX3"
    client_secret = "uBEGX8nUr4"
    encText = urllib.parse.quote("야구")
    url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
    return(response_body.decode('utf-8'))

if __name__ == '__main__':
    print(news())