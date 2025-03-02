import streamlit as st
import processor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the page
st.set_page_config(layout="wide", page_title="WhatsApp Chat Analyzer", page_icon="💬")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")

# Apply CSS for Dark Mode
if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #121212;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #1E1E1E;
        }
        .stMarkdown, .stTextInput, .stSelectbox, .stButton, .stMetric {
            color: white !important;
        }
        .title {
            font-size: 50px !important;
            font-family: 'Arial', sans-serif;
            color: #1DB954 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .title {
            font-size: 50px !important;
            font-family: 'Arial', sans-serif;
            color: #FF5733 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Title with Dark Mode Support
st.markdown('<h1 class="title">WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)
st.write("This app helps you to analyze your WhatsApp chat 📊")

# Sidebar Upload
st.sidebar.title("WELCOME")
uploaded_file = st.sidebar.file_uploader("📂 Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = processor.preproccess(data)

    # User Selection
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("🔍 Show analysis for", user_list)

    # Stats Area
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_video, num_image, links, num_audio = helper.fetch_stats(selected_user, df)
        st.title("📊 Chat Statistics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("📩 Messages", num_messages)
        col2.metric("📝 Words", words)
        col3.metric("🔗 Links", links)
        col4.metric("🎥 Videos", num_video)
        col5.metric("📷 Images", num_image)
        col6.metric("🎵 Audios", num_audio)

        # Monthly Timeline
        st.title("📆 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        ax.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        ax.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Weekly Activity Map
        st.title("📊 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(user_heatmap)
        st.pyplot(fig)

         # Most COmmon Words
        st.title(" Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        if not most_common_words.empty:
            st.dataframe(most_common_words)
        else:
            st.write("No words found in chat!")
            
            
       

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("😀 Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Emoji Usage Data")
            if not emoji_df.empty:
                st.dataframe(emoji_df, width=300)  # Set width for better layout
            else:
                st.write("No emojis found in chat!")

        with col2:
            st.subheader("Top Emojis Used")
            if not emoji_df.empty and len(emoji_df) >= 1:
                fig, ax = plt.subplots()
                top_n = min(5, len(emoji_df))  # Avoid indexing errors if less than 5 emojis
                colors = plt.cm.Paired.colors[:top_n]  # Apply better colors
                ax.pie(emoji_df.iloc[:top_n, 1], labels=emoji_df.iloc[:top_n, 0], autopct="%0.2f%%", colors=colors)
                ax.axis("equal")  # Keep pie chart circular
                st.pyplot(fig)
            else:
                st.write("Not enough emojis to display a pie chart!")
