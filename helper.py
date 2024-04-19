from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()

def fetch_stats(user, df):
    

    if user != "Overall":
        df = df[df['user'] == user]

    # no of messsages
    num_messages =  df.shape[0]

    # no. of words
    words = []
    for message in df['message']:
        words.extend(message.split(" "))
    num_words = len(words)

    # fetch media messages
    num_mms = df[df['message'] == "<Media omitted>\n"].shape[0]

    # number of Links Shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)


    return num_messages, num_words, num_mms, num_links
    
def fetch_active_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={
        'index':'name', 'user':'percent'
        })
    return x, df_percent

def create_wordcloud(user,df):
    if user != "Overall":
        df = df[df['user'] == user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]

    f = open("./stop_hinglish.txt",'r')
    stop_words = f.read()
    f.close()
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
        
    wc = WordCloud(width=200, height=200,
                    min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]

    f = open("./stop_hinglish.txt",'r')
    stop_words = f.read()
    f.close()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    from collections import Counter
    common_words = pd.DataFrame(Counter(words).most_common(20),
                                columns=['words','count'])

    return common_words

def emoji_analysis(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    emojis=[]
    #emoji list
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),
                            columns=['emoji', 'count'])
    # return emoji_df
    return emoji_df

def monthly_timeline(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+' - '+str(timeline['year'][i]))
        
    timeline['time'] = time
    return timeline

def day_timeline(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    timeline = df.groupby(df['date'].dt.date).count()['message'].reset_index()
    
    return timeline

def activity_map_weekly(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    timeline = df.groupby(df['date'].dt.day_name()).count()['message'].reset_index()
    
    return timeline

def activity_map_monthly(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    timeline = df.groupby(df['month']).count()['message'].reset_index()
    
    return timeline
    
    

    