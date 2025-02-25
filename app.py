import streamlit as st 
import processor ,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analsis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=processor.preproccess(data)
    

    


    # fetch uinique user

    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    # Stats Area
    st.title("Top Statistics")
    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_video, num_image, links,num_audio = helper.fetch_stats(selected_user,df)

        
        
        col1, col2, col3, col4 , col5 ,col6 = st.columns(6)
        
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words \n")
            st.title(words)
        
        with col3:
            st.header("Links Shared")
            st.title(links)
        with col4:
            st.header("Video Shared")
            st.title(num_video)
        with col5:
            st.header("Image Shared")
            st.title(num_image)
        with col6:
            st.header("Audio Shared")
            st.title(num_audio)

        # monthly  timeline
        st.title("Monthly Timeline")

        timeline=helper.monthly_timeline(selected_user,df)

        fig , ax =plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # daily timeline

        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Activity map


        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)

            fig, ax = plt.subplots()

            ax.bar(busy_day.index , busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)

            fig, ax = plt.subplots()

            ax.bar(busy_month.index, busy_month.values )
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # A
        st.title("Weekly Activity map")
        user_heatmap=helper.activity_heat_map(selected_user,df)
        plt.figure(figsize=(10, 4))
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                
                
         # Wordcloud
        st.title("WordCloud")    
        df_wc=helper.create_wordcloud(selected_user,df)
        fig , ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)

        fig , ax =plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
            else:
                st.write("No emojis found in chat!")


