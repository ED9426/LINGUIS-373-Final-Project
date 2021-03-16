# --== DataRetrieve Header ==--
# Author: Edward Zhao
# Email: edward.zhao@wisc.edu
# Description: This script retrieves all the speech from 
# https://www.rev.com/blog/transcript-category/congressional-testimony-hearing-transcripts
# and saves data in a csv file named "Congressional Testimony & Hearing Transcripts.csv"

import requests
import bs4
import pandas as pd

# list to save transcript data
data = []
# generate the page url of transcripts
for page_number in range(16):
    page_url = "https://www.rev.com/blog/transcript-category/congressional-testimony-hearing-transcripts"
    if (page_number != 0):
        page_url += "/page/" + str(page_number+1)
    # retrieve the urls of transcripts from the current page
    html = bs4.BeautifulSoup(requests.get(page_url).text, "html.parser")
    transcript_urls = html.find("div", class_="fl-post-grid").find_all("a", href=True)
    for transcript_url in transcript_urls:
        html = bs4.BeautifulSoup(requests.get(transcript_url['href']).text, "html.parser")
        # retrieve the data from the current trascript
        data.append(html.find("div", class_="fl-callout-text").find_all("p"))

# lists used to save speakers their speech
speaker = []
speech = []
# save data to two lists 
for i in range(len(data)):
    for j in range(len(data[i])):
        if (len(data[i][j]) > 1):
            temp = []
            for k in data[i][j]:
                temp.append(k)
            speaker.append(temp[0])
            speech.append(temp[-1])

# process the format of data
for i in range(len(speaker)):
    speaker[i] = speaker[i].split(":")[0]
    speech[i] = speech[i][1:]
# convert to dictionary
df = pd.DataFrame({'Speaker': speaker, 'Speech': speech})
# saving the dataframe
df.to_csv('Congressional Testimony & Hearing Transcripts.csv', index = False, encoding='utf-8-sig')