# imports
import pandas as pd
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

st.markdown("<h1 style='text-align: center; color: white;'>Poker Web3 Feasibility - Gamesight</h1>", unsafe_allow_html=True)

# import dfs
df_streamers = pd.read_csv(
    './data/fun_country_poker_streamers.csv',
    )
df_streamers_gambling = pd.read_csv(
    './data/fun_country_gambling_streamers.csv'
)
df_ma_crypto = pd.read_csv(
    './data/gambling_stats_crypto.tsv',
    sep='\t',
    index_col = 'franchise_name'
)
df_ma_crypto.columns = [ 'Channel Count', 'Stream Count', 'Viewer Hours', 'Streamed Hours']

# add columns cus I goofed
df_streamers.columns = [
    'ChannelID', 'Twitch Profile', 'Twitter Profile', 'YouTube Profile',
    'Instagram Profile', 'Contro Creator', 'YouTube Linked Geos', 'Geo (Gamesight)',
    'Geo (Language)', 'Geo (Language Broadcaster)', 'Geo (Tagged)', 'Have creator geo?',
    'Geo (YouTube)', 'Geo (Twitter)', 'Language (Twitch)', 'Broadcaster Languge (Twitch)',
    'Tagged Geos', 'Channel ACV Deviation', 'Percent of content is gaming', '#Streams (Channel)',
    '#Hours Streamed (Channel)', 'Last Stream (Channel)', 'Mature Warning', 'Peak CCV (Channel)',
    'Peak CCV (Target)', 'Cost (Only Stream)', 'Cost (Only social estimated)', 'Cost (Only social Twitter)',
    'Twitch name', 'YouTube ID', 'Instagram Profile2', 'GsID', 'YouTube Name',
    'Twitter Name', '#Followers (Twitter)', 'Contact email', 'Approved?',
    'Approval Comments', '#Followers (Twitch)', 'ACV (Channel)', '#Games (Channel)',
    'Estimated Cost: $0', 'Games Played (Target)', '#Games (Target)', '#Streams (Target)',
    '#Hours Streamed (Target)', 'Last Stream (Target)', 'ACV (Target)', '% ACV Drop (Non-target to Target)',
    'Primary Game Name', 'ACV (Primary Game)', '% ACV Drop (Primary to Non-Primary)', '% Time spent streaming Primary Game',
    'Trending Score', 'Engagement Score', 'Loyalty Score', 'Reach Score',
    'Audience Retention Score', 'Influence Score', 'Viewer Engagement Score', 'Streamed Crypto?'
]
df_streamers_gambling.columns =  [
    'ChannelID', 'Twitch Profile', 'Twitter Profile', 'YouTube Profile',
    'Instagram Profile', 'Contro Creator', 'YouTube Linked Geos', 'Geo (Gamesight)',
    'Geo (Language)', 'Geo (Language Broadcaster)', 'Geo (Tagged)', 'Have creator geo?',
    'Geo (YouTube)', 'Geo (Twitter)', 'Language (Twitch)', 'Broadcaster Languge (Twitch)',
    'Tagged Geos', 'Channel ACV Deviation', 'Percent of content is gaming', '#Streams (Channel)',
    '#Hours Streamed (Channel)', 'Last Stream (Channel)', 'Mature Warning', 'Peak CCV (Channel)',
    'Peak CCV (Target)', 'Cost (Only Stream)', 'Cost (Only social estimated)', 'Cost (Only social Twitter)',
    'Twitch name', 'YouTube ID', 'Instagram Profile2', 'GsID', 'YouTube Name',
    'Twitter Name', '#Followers (Twitter)', 'Contact email', 'Approved?',
    'Approval Comments', '#Followers (Twitch)', 'ACV (Channel)', '#Games (Channel)',
    'Estimated Cost: $0', 'Games Played (Target)', '#Games (Target)', '#Streams (Target)',
    '#Hours Streamed (Target)', 'Last Stream (Target)', 'ACV (Target)', '% ACV Drop (Non-target to Target)',
    'Primary Game Name', 'ACV (Primary Game)', '% ACV Drop (Primary to Non-Primary)', '% Time spent streaming Primary Game',
    'Trending Score', 'Engagement Score', 'Loyalty Score', 'Reach Score',
    'Audience Retention Score', 'Influence Score', 'Viewer Engagement Score', 'Streamed Crypto?'
]

# Format Poker Columns / cleaning
df_streamers = df_streamers.iloc[2:]
df_streamers['Streamed Crypto?'] = df_streamers['Streamed Crypto?'].apply(lambda x: True if len(str(x))>3 else False)
df_streamers['ACV (Target)'] = df_streamers['ACV (Target)'].str.replace(',','').astype(int)
df_streamers_formatted = df_streamers[['Twitch Profile', 'Streamed Crypto?','ACV (Target)', '#Streams (Target)', 'Primary Game Name' ]]

df_streamers_gambling['Streamed Crypto?'] = df_streamers_gambling['Streamed Crypto?'].apply(lambda x: True if len(str(x))>3 else False)
df_streamers_gambling['ACV (Target)'] = df_streamers_gambling['ACV (Target)'].str.replace(',','').astype(int)
df_streamers_gambling_formatted = df_streamers_gambling[['Twitch Profile', 'Streamed Crypto?','ACV (Target)', '#Streams (Target)', 'Primary Game Name' ]]

# market analysis dfs
df_ma = pd.DataFrame(
    [
        [ 6520, 36032, 34566989, 102772],
        [ 2168, 11559,	7051508, 29579],
        [ 4393,	24248,	5800939, 68609]
    ],
    columns= [ 'Channel Count', 'Stream Count', 'Viewer Hours', 'Streamed Hours'],
    index=['slots', 'virtual casino', 'poker']
)


# initial columns
col_1, col_2, col_3 = st.columns(3)

with col_1:
    st.metric(
        '# of Poker Streamers',
        len(df_streamers)
    )
    st.metric(
        '# of Gambling Streamers',
        len(df_streamers_gambling)
    )
with col_2:
    st.metric(
        '# of Crypto-friendly Poker Streamers',
        len(df_streamers[df_streamers['Streamed Crypto?']==True])
    )
    st.metric(
        '# of Crypto-friendly Gambling Streamers',
        len(df_streamers_gambling[df_streamers_gambling['Streamed Crypto?']==True])
    )
with col_3:
    st.metric(
        '# of Crypto-friendly Poker Streamers',
        str(round(len(df_streamers[df_streamers['Streamed Crypto?']==True])/len(df_streamers),4) * 100) + '%'
    )
    st.metric(
        '# of Crypto-friendly Gambling Streamers',
        str(round(len(df_streamers_gambling[df_streamers_gambling['Streamed Crypto?']==True])/len(df_streamers_gambling),4) * 100) + '%'
    )
#st.dataframe(df_ma_crypto)
#st.dataframe(df_ma)
df_ma['Streamed Crypto?'] = False
df_ma_crypto['Streamed Crypto?'] = True
df_ma_merged = pd.concat([df_ma_crypto, df_ma])
#st.dataframe(df_ma_merged)

# create plotly grouped pie charts
slots_df = df_ma_merged[df_ma_merged.index == 'slots']
virtual_casino_df = df_ma_merged[df_ma_merged.index == 'virtual casino']
poker_df = df_ma_merged[df_ma_merged.index == 'poker']
st.markdown("<h3 style='text-align: center; color: white;'>Crypto-Friendly Streamer Viewer Hours</h3>", unsafe_allow_html=True)
config = {'displayModeBar': False}


pie_1, pie_2, pie_3 = st.columns(3)

with pie_1:
    st.metric('Poker Crypto-Friendly Viewer Hours', '{:,}'.format(int(poker_df[poker_df['Streamed Crypto?'] == True]['Viewer Hours'])))
    fig_bar1 = px.pie(poker_df,
    values='Viewer Hours', color = slots_df['Streamed Crypto?']
    )
    fig_bar1.update_layout(height=250,margin=dict(l=20, r=20, t=0, b=0))
    st.plotly_chart(fig_bar1, use_container_width=True, config=config)
    

with pie_2:
    st.metric('Slots Crypto-Friendly Viewer Hours', '{:,}'.format(int(slots_df[slots_df['Streamed Crypto?'] == True]['Viewer Hours'])))
    fig_bar2 = px.pie(slots_df,
    values='Viewer Hours', color = slots_df['Streamed Crypto?']
    )
    fig_bar2.update_layout(height=250,margin=dict(l=20, r=20, t=0, b=0))
    st.plotly_chart(fig_bar2, use_container_width=True, config=config)
with pie_3:
    st.metric('VC Crypto-Friendly Viewer Hours', '{:,}'.format(int(virtual_casino_df[virtual_casino_df['Streamed Crypto?'] == True]['Viewer Hours'])))
    fig_bar3 = px.pie(virtual_casino_df,
    values='Viewer Hours', color = virtual_casino_df['Streamed Crypto?']
    )
    fig_bar3.update_layout(height=250,margin=dict(l=20, r=20, t=0, b=0))
    st.plotly_chart(fig_bar3, use_container_width=True, config=config)


# DROPDOWN MENU
with st.expander('Poker-exclusive Streamers Spreadsheet'):
    st.dataframe(df_streamers_formatted)

with st.expander('All Gambling Streamers Spreadsheet'):
    st.dataframe(df_streamers_gambling_formatted)
