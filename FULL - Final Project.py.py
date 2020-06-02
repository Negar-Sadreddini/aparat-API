import requests
import json, csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

informative_url = 'https://www.aparat.com/api#videobytag'
# This is a link which explains how we can extract data from Aparat's API, By reading it we decided to scrap Aparat's videos by their defferent tags(videobytag).

url_sports = 'https://www.aparat.com/etc/api/videobytag/text/%D9%88%D8%B1%D8%B2%D8%B4%DB%8C'
url_educational = 'https://www.aparat.com/etc/api/videobytag/text/%D8%A2%D9%85%D9%88%D8%B2%D8%B4%DB%8C'
url_nature = 'https://www.aparat.com/etc/api/videobytag/text/%DA%AF%D8%B1%D8%AF%D8%B4%DA%AF%D8%B1%DB%8C'
url_entertainment = 'https://www.aparat.com/etc/api/videobytag/text/%D8%AA%D9%81%D8%B1%DB%8C%D8%AD%DB%8C'
url_funny = 'https://www.aparat.com/etc/api/videobytag/text/%D8%B7%D9%86%D8%B2'
urls = [url_sports,url_educational,url_nature,url_entertainment,url_funny]
n = int(input('Number of pages')) # n is the number of pages we evaluate for each tag. Each page gives us information for 20 videos.

results = []
for url in urls:
    for count in range(n):
        print(count)
        raw = requests.get(url = url)
        response = raw.json()
        # Response is a dictionary that it's first key's(videobytag) value, is a list of dictionaries of videos different information such as title,visit_cnt and duration.
        url = response['ui']['pagingForward']
        time.sleep(0.3)  # We need to make halt in web scraping in order to avoid getting error and dropping out of the website!
        for value in response['videobytag']:
            results.append(value)
#print(results)  # Results is a list of all information about all the videos. items of this list are dictionaries.
title_list,duration_list,visit_cnt_list = [],[],[]
for dict in results:
    title_list.append(dict['title'])
    duration_list.append(dict['duration'])
    visit_cnt_list.append(dict['visit_cnt'])

df_dict = {'sports_title':title_list[0:(n*20)],'sports_duration':duration_list[0:(n*20)],'sports_visit_cnt':visit_cnt_list[0:(n*20)], \
'education_title':title_list[(n*20):(n*2*20)],'education_duration':duration_list[(n*20):(n*2*20)],'education_visit_cnt':visit_cnt_list[(n*20):(n*2*20)], \
'nature_title':title_list[(n*2*20):(n*3*20)],'nature_duration':duration_list[(n*2*20):(n*3*20)],'nature_visit_cnt':visit_cnt_list[(n*2*20):(n*3*20)], \
'entertainment_title':title_list[(n*3*20):(n*4*20)],'entertainment_duration':duration_list[(n*3*20):(n*4*20)],'entertainment_visit_cnt':visit_cnt_list[(n*3*20):(n*4*20)], \
'funny_title':title_list[(n*4*20):(n*5*20)],'funny_duration':duration_list[(n*4*20):(n*5*20)],'funny_visit_cnt':visit_cnt_list[(n*4*20):(n*5*20)]}
df = pd.DataFrame(df_dict)
print(df[df['sports_visit_cnt'] == max(df['sports_visit_cnt'])]['sports_title'])
print(df[df['education_visit_cnt'] == max(df['education_visit_cnt'])]['education_title'])
print(df[df['nature_visit_cnt'] == max(df['nature_visit_cnt'])]['nature_title'])
print(df[df['entertainment_visit_cnt'] == max(df['entertainment_visit_cnt'])]['entertainment_title'])
print(df[df['funny_visit_cnt'] == max(df['funny_visit_cnt'])]['funny_title'])

plt.bar(['Sports','Education','Nature','Entertainment','Funny'],[np.mean(df['sports_visit_cnt']),np.mean(df['education_visit_cnt']),np.mean(df['nature_visit_cnt']), \
np.mean(df['entertainment_visit_cnt']),np.mean(df['funny_visit_cnt'])],width=0.8)
plt.title('Comparision between Tags popularity')
plt.xlabel('Tags')
plt.ylabel('Mean Popularity')
plt.savefig('General collation barchart.png')
plt.show()

# With the help of scatter plot we can find outlyer data, and also general pattern!
plt.subplot(2,3,1)
plt.scatter(df['sports_duration'],df['sports_visit_cnt'],color='pink',label='For Sports')
plt.title('Sports')
plt.xlabel('Duration(s)')
plt.ylabel('Visit Count')
plt.legend()
plt.subplot(2,3,2)
plt.scatter(df['education_duration'],df['education_visit_cnt'],color='blue',alpha=.2,label='For Education')
plt.title('Education')
plt.xlabel('Duration(s)')
plt.legend()
plt.subplot(2,3,3)
plt.scatter(df['funny_duration'],df['funny_visit_cnt'],color='red',alpha=0.4,label='For Funny')
plt.title('Funny')
plt.xlabel('Duration(s)')
plt.legend()
plt.subplot(2,3,4)
plt.scatter(df['entertainment_duration'],df['entertainment_visit_cnt'],color='purple',alpha=0.4,label='For Entertainment')
plt.title('Entertainment')
plt.xlabel('Duration(s)')
plt.ylabel('Visit Count')
plt.legend()
plt.subplot(2,3,5)
plt.scatter(df['nature_duration'],df['nature_visit_cnt'],color='green',label='For Nature',alpha=0.2)
plt.title('Nature')
plt.xlabel('Duration(s)')
plt.legend()
plt.savefig('General scatter plots for each tag.png')
plt.show()


# Now we need to level duration, in order to evaluate the impact of video's duration on it's view count:
def leveling(n):
    if n <= 20:
        n = 'too short'
    elif n>15 and n<=60:
        n = 'short'
    elif n>60 and n<=180:
        n = 'medium'
    elif n>180 and n<=900:
        n = 'long'
    else:
        n = 'too long'
    return n

df['sports_duration'] = list(map(lambda x: leveling(x),df['sports_duration']))
df['entertainment_duration'] = list(map(lambda x: leveling(x),df['entertainment_duration']))
df['education_duration'] = list(map(lambda x: leveling(x),df['education_duration']))
df['nature_duration'] = list(map(lambda x: leveling(x),df['nature_duration']))
df['funny_duration'] = list(map(lambda x: leveling(x),df['funny_duration']))

sports_duration = df.groupby('sports_duration').groups
sports_too_short_mean = np.mean([df.loc[value]['sports_visit_cnt'] for value in sports_duration['too short']])
sports_short_mean = np.mean([df.loc[value]['sports_visit_cnt'] for value in sports_duration['short']])
sports_medium_mean = np.mean([df.loc[value]['sports_visit_cnt'] for value in sports_duration['medium']])
sports_long_mean = np.mean([df.loc[value]['sports_visit_cnt'] for value in sports_duration['long']])
sports_too_long_mean = np.mean([df.loc[value]['sports_visit_cnt'] for value in sports_duration['too long']])

education_duration = df.groupby('education_duration').groups
education_too_short_mean = np.mean([df.loc[value]['education_visit_cnt'] for value in sports_duration['too short']])
education_short_mean = np.mean([df.loc[value]['education_visit_cnt'] for value in education_duration['short']])
education_medium_mean = np.mean([df.loc[value]['education_visit_cnt'] for value in education_duration['medium']])
education_long_mean = np.mean([df.loc[value]['education_visit_cnt'] for value in education_duration['long']])
education_too_long_mean = np.mean([df.loc[value]['education_visit_cnt'] for value in education_duration['too long']])

nature_duration = df.groupby('nature_duration').groups
nature_too_short_mean = np.mean([df.loc[value]['nature_visit_cnt'] for value in nature_duration['too short']])
nature_short_mean = np.mean([df.loc[value]['nature_visit_cnt'] for value in nature_duration['short']])
nature_medium_mean = np.mean([df.loc[value]['nature_visit_cnt'] for value in nature_duration['medium']])
nature_long_mean = np.mean([df.loc[value]['nature_visit_cnt'] for value in nature_duration['long']])
nature_too_long_mean = np.mean([df.loc[value]['nature_visit_cnt'] for value in nature_duration['too long']])

entertainment_duration = df.groupby('entertainment_duration').groups
entertainment_too_short_mean = np.mean([df.loc[value]['entertainment_visit_cnt'] for value in entertainment_duration['too short']])
entertainment_short_mean = np.mean([df.loc[value]['entertainment_visit_cnt'] for value in entertainment_duration['short']])
entertainment_medium_mean = np.mean([df.loc[value]['entertainment_visit_cnt'] for value in entertainment_duration['medium']])
entertainment_long_mean = np.mean([df.loc[value]['entertainment_visit_cnt'] for value in entertainment_duration['long']])
entertainment_too_long_mean = np.mean([df.loc[value]['entertainment_visit_cnt'] for value in entertainment_duration['too long']])

funny_duration = df.groupby('funny_duration').groups
funny_too_short_mean = np.mean([df.loc[value]['funny_visit_cnt'] for value in funny_duration['too short']])
funny_short_mean = np.mean([df.loc[value]['funny_visit_cnt'] for value in funny_duration['short']])
funny_medium_mean = np.mean([df.loc[value]['funny_visit_cnt'] for value in funny_duration['medium']])
funny_long_mean = np.mean([df.loc[value]['funny_visit_cnt'] for value in funny_duration['long']])
funny_too_long_mean = np.mean([df.loc[value]['funny_visit_cnt'] for value in funny_duration['too long']])

plt.subplot(2,3,1)
plt.bar(['Too Short','Short','Medium','Long','Too Long'],[sports_too_short_mean,sports_short_mean,sports_medium_mean,sports_long_mean,sports_too_long_mean])
plt.title('Sports')
plt.subplot(2,3,2)
plt.bar(['Too Short','Short','Medium','Long','Too Long'],[education_too_short_mean,education_short_mean,education_medium_mean,education_long_mean,education_too_long_mean])
plt.title('Education')
plt.subplot(2,3,3)
plt.bar(['Too Short','Short','Medium','Long','Too Long'],[nature_too_short_mean,nature_short_mean,nature_medium_mean,nature_long_mean,nature_too_long_mean])
plt.title('Nature')
plt.subplot(2,3,4)
plt.bar(['Too Short','Short','Medium','Long','Too Long'],[entertainment_too_short_mean,entertainment_short_mean,entertainment_medium_mean,entertainment_long_mean,entertainment_too_long_mean])
plt.title('Entertainment')
plt.subplot(2,3,5)
plt.bar(['Too Short','Short','Medium','Long','Too Long'],[funny_too_short_mean,funny_short_mean,funny_medium_mean,funny_long_mean,funny_too_long_mean])
plt.title('Funny')
plt.savefig('General barcharts for the relation of duration and visit count for each label.png')
plt.show()


#sns.jointplot(x=df[['sports_duration']],y=df['sports_visit_cnt'],data=df,kind='kde')
#plt.show()





