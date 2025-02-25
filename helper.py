from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    
    # ✅ Clean hidden characters
    df['message'] = df['message'].str.replace(r'[\u200E\u202F\uFEFF]', '', regex=True).str.strip()
    
     # ✅ Improved media message filtering
    num_image = df[df['message'].str.contains(r'image omitted', na=False, case=False)].shape[0]
    num_video = df[df['message'].str.contains(r'video omitted', na=False, case=False)].shape[0]
    num_audio = df[df['message'].str.contains(r'audio omitted', na=False, case=False)].shape[0]

   # fetch number of links shared
    links = []
    
    for message in df['message']:
        links.extend(extract.find_urls(message))
        

    return num_messages, len(words), num_video, num_image, len(links),num_audio


def most_busy_user(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percentage'})
    
    return x, df


def create_wordcloud(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

        # List of unwanted phrases (use partial matching)
    unwanted_phrases = [
        "image omitted",
        "video omitted",
        "audio omitted",
        "GIF omitted",
        "sticker omitted",
        "Missed voice call",
        "You blocked this contact",
        "You unblocked this contact",
        "Messages and calls are end-to-end encrypted",
        "Disappearing messages were turned off",
        "Contact card omitted",
        "This message was deleted",
        "This message was edited",
        "You were added",
        "created this group"
    ]

    # Remove messages that contain any of the unwanted phrases
    pattern = "|".join(unwanted_phrases)
    df= df[~df['message'].str.contains(pattern, case=False, na=False)]

    wc=WordCloud(width=500,height=500 , min_font_size=10 , background_color='white')
    
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    
    return df_wc



#most common words

def most_common_words(selected_user,df):

    f=open('stopwords_hienglish.txt','r')
    stop_words = f.read()


    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['message'] = df['message'].astype(str).str.strip()

        # List of unwanted phrases (use partial matching)
    unwanted_phrases = [
            "image omitted",
            "video omitted",
            "audio omitted",
            "GIF omitted",
            "sticker omitted",
            "Missed voice call",
            "You blocked this contact",
            "You unblocked this contact",
            "Messages and calls are end-to-end encrypted",
            "Disappearing messages were turned off",
            "Contact card omitted",
            "This message was deleted",
            "This message was edited",
            "You were added",
            "created this group"
    ]

    # Remove messages that contain any of the unwanted phrases
    pattern = "|".join(unwanted_phrases)
    temp = df[~df['message'].str.contains(pattern, case=False, na=False)]


    print(stop_words)

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []  # Renamed to avoid conflicts

    for message in df['message']:  # Convert messages to string to avoid errors
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])  # Extract emojis
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df



def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline



def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()



def activity_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name' , columns='period' , values='message', aggfunc='count').fillna(0)

    return user_heatmap




