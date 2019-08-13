import pandas as pd
import requests
import xlsxwriter
from bs4 import BeautifulSoup
img_list = []
links_list = []
new_links_list = []
img_links_list = []
view_count_list = []
likes_list = []
dislikes_list = []
title_list = []
try:
    response = requests.get("https://www.youtube.com/feed/trending")
    html_data = response.content
    soup = BeautifulSoup(html_data, 'html.parser')

    # finding videos links
    for links in soup.find_all('a'):
        links_response = links.get('href')
        if links_response.startswith("/watch"):
            links_list.append("https://youtube.com"+links_response)
    for i in range(0, len(links_list), 2):
        new_links_list.append(links_list[i])

    # creating files for images
    for i in range(len(new_links_list)):
        img_list.append(str(i+1)+".jpg")

    # finding images links
    for img in soup.find_all('img'):
        if img.get('data-thumb') != None and img.get('data-thumb').startswith("https://i.ytimg.com/"):
            img_links_list.append(img.get('data-thumb'))
        if img.get('src') != None and img.get('src').startswith("https://i.ytimg.com/"):
            img_links_list.append(img.get('src'))

    # finding title, views, likes, dislikes count
    for each_video in new_links_list:
        single_response = requests.get(each_video)
        single_html_data = single_response.content
        single_soup = BeautifulSoup(single_html_data, 'html.parser')
        for views in single_soup.find_all('div', attrs={"class": "watch-view-count"}):
            view_count_list.append(views.next)
        for likes in single_soup.find_all('button'):
            if likes.get('aria-label') != None and likes.get('aria-label').startswith("like this"):
                temp1 = (likes.get('aria-label').split(' '))[5]
        likes_list.append(temp1)
        for dislikes in single_soup.find_all('button'):
            if dislikes.get('aria-label') != None and dislikes.get('aria-label').startswith("dislike this"):
                temp2 = dislikes.get('aria-label').split(' ')[5]
        dislikes_list.append(temp2)
        for title in single_soup.find_all('title'):
            title_list.append(title.next)

    for i in range(len(new_links_list)):
        print("Title :", title_list[i])
        print("Video link :", new_links_list[i])
        print("Video image link :", img_links_list[i])
        file = open(img_list[i], 'wb')
        file.write(requests.get(img_links_list[i]).content)
        print("Views count - ", view_count_list[i])
        print("Likes - ", likes_list[i])
        print("Dislikes - ", dislikes_list[i])
        print("\n\n")

    # saving the data into a excel file
    df = pd.DataFrame({'Title': title_list, 'Video link': new_links_list, 'Likes': likes_list, 'Dislikes': dislikes_list, 'Views': view_count_list , 'Image link': img_links_list})
    writer = pd.ExcelWriter('youtube_data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
except Exception as err:
    print(err)

