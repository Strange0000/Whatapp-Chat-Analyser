import pandas as pd
import re

def preproccess(data):
    pattern = r'\[\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\s?[APM]*\]\s*'
    message=re.split(pattern , data)[1:]
    dates=re.findall(pattern , data)
    df=pd.DataFrame({'user_message':message , 'message_date':dates})
    
    
    df['message_date'] = df['message_date'].astype(str)

#  Remove brackets and unexpected characters
    df['message_date'] = df['message_date'].str.replace(r'[\[\]\u202f]', '', regex=True)

#  Trim spaces
    df['message_date'] = df['message_date'].str.strip()

#  Ensure a space before AM/PM
    df['message_date'] = df['message_date'].str.replace(r'(\d)(AM|PM)', r'\1 \2', regex=True)

# ✅ Step 4: Convert to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M:%S %p")
    
    
    
    users=[]
    messages=[]


    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:] :
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group notification")
            message.append(entry[0])
            
          

    df['users']=users
    df['message']=messages
    df['message'] = df['message'].str.replace(r'[\u200E\u202F\uFEFF]', '', regex=True)

    df.drop(columns=['user_message'] , inplace=True)

    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['day']=df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['month_num'] = df['message_date'].dt.month # monthly timeline

    df['day_name'] = df['message_date'].dt.day_name() #Activity map

    df['only_date'] = df['message_date'].dt.date # daily timline



    # for heat map

    period = []  # Define an empty list for storing time periods

    for hours in df[['day_name', 'hour']]['hour']:
        if hours == 23:
            period.append(str(hours) + "-" + str(0))  # Convert 0 to string properly
        elif hours == 0:  # ✅ Use 0 instead of 00
            period.append(str(hours) + "-" + str(hours + 1))
        else:
            period.append(str(hours) + "-" + str(hours + 1))

    df['period'] = period  # Add the period column to the DataFrame
    return df  # Return the modified DataFrame


