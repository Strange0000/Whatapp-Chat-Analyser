# WhatsApp Chat Analysis




## Overview

WhatsApp Chat Analysis is a data-driven tool that helps users extract insights from their WhatsApp chat history. Built using Streamlit, Matplotlib, Seaborn, and Python, this app provides detailed statistics such as message count, word count, media shared, activity trends, common words, and emoji usage.

## Features

✅ Upload WhatsApp Chat Export (.txt)
✅ View Top Statistics: Messages, Words, Links, Videos, Images, and Audio shared
✅ Activity Timeline: Monthly and Daily trends
✅ User Activity Map: Weekly heatmap, busiest days, and most active users
✅ Most Common Words & WordCloud
✅ Emoji Analysis

## Installation


## Clone the repository

git clone https://github.com/Strange0000/whatsapp-chat-analysis.git
cd whatsapp-chat-analysis


Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


## Install dependencies
pip install -r requirements.txt


## Usage

Run the Streamlit app:
streamlit run app.py

## How to Export WhatsApp Chat?

Open WhatsApp on your phone.
Go to the chat you want to analyze.
Tap More Options (⋮) > Export Chat.
Choose Without Media for a cleaner analysis.
Save the .txt file and upload it to the app.


## Folder Structure

whatsapp-chat-analysis/
│── processor.py        # Chat preprocessing functions

│── helper.py           # Analysis and visualization functions

│── app.py              # Streamlit app main script

│── requirements.txt    # Dependencies

│── README.md           # Project documentation


## Dependencies


Python 3.x

Streamlit

Matplotlib

Seaborn

Pandas

Numpy



## Future Improvements


✅ Sentiment Analysis

✅ NLP-based Chat Summarization

✅ Advanced Visualization & Analytics



## Contributing
Feel free to open issues or create pull requests to contribute to this project.

License
This project is open-source under the MIT License.
