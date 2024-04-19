from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
import preprocessor
import helper
import emoji


st.set_page_config(layout="wide")

st.sidebar.title("""
                Whatsapp Chat Analyzer
                 """)
with st.sidebar:
    # uploaded_file = None
    # if uploaded_file is None:
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
        
        user = st.selectbox("Show Analysis wrt",
                     user_list)
        
        
        

if uploaded_file is not None:

    if st.sidebar.button("Show Analysis"):

        num_messages, num_words, num_mms, num_links = helper.fetch_stats(user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_mms)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Display Timeline
        st.title("Timeline")
        col1, col2 = st.columns(2)
        #Weekly
        with col1:
            st.subheader("Monthly")
            monthly_timeline = helper.monthly_timeline(user,df)
            fig = px.line(monthly_timeline, y='message', x='time')
            st.plotly_chart(fig)

        #Daily
        with col2:
            st.subheader("Daily")
            day_timeline = helper.day_timeline(user,df)
            fig = px.line(day_timeline, y='message', x='date')
            st.plotly_chart(fig)

        #Display Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Weekly")
            activity = helper.activity_map_weekly(user,df)
            fig = px.bar(activity, y='message', x='date')
            fig.update_layout(barmode='stack', xaxis = {'categoryorder':'total descending'})
            st.plotly_chart(fig)
        with col2:
            st.subheader("Monthly")
            activity = helper.activity_map_monthly(user,df)
            fig = px.bar(activity, y='message', x='month')
            fig.update_layout(barmode='stack', xaxis = {'categoryorder':'total descending'})
            st.plotly_chart(fig)

        if user=="Overall":
            st.title("Most Active Users")
            x, df_percent = helper.fetch_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(df_percent)

        # Generate Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        st.title("Most Common Words")
        common_words_df = helper.most_common_words(user, df)
        fig = px.bar(common_words_df, x = common_words_df['count'], y = common_words_df['words'])
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)

        # Emoji Analysis
        st.title("Emojis Used")
        emoji_df = helper.emoji_analysis(user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            fig = px.pie(emoji_df['count'].head(), names=emoji_df['emoji'].head())
            st.plotly_chart(fig)
    else:
        st.title("Press Show Analysis")

