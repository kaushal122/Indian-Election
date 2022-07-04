import pandas as pd
import streamlit as st
import plotly.express as px
from resultDataframe import *

st.set_page_config(layout="wide")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
    animation_symbol='❄'
st.markdown(f"""<div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>
                <div class="snowflake">{animation_symbol}</div>""",unsafe_allow_html=True)




href = ['ResultAcByeNov2021/partywiseresult-S01.htm','ResultAcGenMar2022/partywiseresult-S05.htm', 'ResultAcByeMar2022/partywiseresult-S03.htm']
text = ['Bye Elections to Assembly Constituency November-2021','GENERAL Elections to Assembly Constituency March-2022','BYE Elections  to Assembly Constituency March-2022']
dict_of_href_text={}
for i in range(0,len(href)):
    dict_of_href_text[text[i]]=href[i]



st.markdown(f'<p class="header">Election Results WebApp</p>',unsafe_allow_html=True)
# st.header("Election Results WebApp")
dict = {"Andhra Pradesh":"S01","Assam":"S03","Bihar":"S04","Goa":"S05","Haryana":"S07","Himachal Pradesh":"S08","Karnataka":"S10","Madhya Pradesh":"S12","Maharashtra":"S13","Manipur":"S14","Meghalaya":"S15","Mizoram":"S16","Nagaland":"S17","Punjab":"S19","Rajasthan":"S20","Uttar Pradesh":"S24","Uttarakhand":"S28","Telangana":"S29","West Bengal":"S25","Dadra & Nagar Haveli And Daman & Diu":"U04"}


state=''

column1,column2=st.columns(2)
with column1:
    st.markdown('<p class="big-font">Select Election</p>', unsafe_allow_html=True)
    # st.subheader("Select Election")
    options = st.selectbox(label="",options=(dict_of_href_text.keys()))
    states=state_names(dict_of_href_text[options])

# constituency_dict = constituencies_dict(dict_of_href_text[options],state)
# st.selectbox(options=['Constituency wise','Party wise'])

# if options==text[2]:
with column2:
    st.markdown(f'<p class="big-font">Select State</p>', unsafe_allow_html=True)
    # st.subheader(options)
    url_1 = dict_of_href_text[options][0:-7]
    state = st.selectbox(label="",options=states)




result_type='Party wise'
if options.find('GENERAL')!=-1 or options.find('General')!=-1:
    st.markdown(f'<p class="big-font">Result Type</p>', unsafe_allow_html=True)
    result_type=st.selectbox(label="",options=['Party wise','Constituency wise'])


if result_type=='Party wise':
    data = state_result(state,url_1)
    data_vote = votes(state,url_1)

    data[['Won', 'Leading', 'Total']] = data[['Won', 'Leading', 'Total']].apply(pd.to_numeric)
    data=data.iloc[:-1,:]
    fig = px.bar(data,x="Party",y="Won",color = "Party",width=600,height=550,title='Seats',color_continuous_scale='Cividis_r',hover_name='Party')

    col1,col2=st.columns(2)
    with col1:
        with st.expander('Show result',expanded=True):
            st.table(data)
            st.plotly_chart(fig)

    #pie chart for votes
    with col2:
        with st.expander("Vote Percentages",expanded = True):
            fig = px.pie(data_vote, values="Vote Percentage", names='Party', title="Vote Percentage",width=500)
            st.table(data_vote)
            st.plotly_chart(fig)



if result_type=='Constituency wise':
    constituency_dict = constituencies_dict(dict_of_href_text[options], state)
    st.markdown(f'<p class="big-font">Select Constituency</p>', unsafe_allow_html=True)
    # st.subheader('Select Constituency')
    constituency = st.selectbox(label="",options=constituency_dict.keys())
    data_candidate_wise =  candidate_wise_result(dict_of_href_text[options],state,constituency_dict[constituency])
    data_candidate_wise[['EVM Votes', 'Postal Votes', 'Total Votes','% of Votes']] = data_candidate_wise[['EVM Votes', 'Postal Votes', 'Total Votes','% of Votes']].apply(pd.to_numeric)
    st.table(data_candidate_wise)
    fig = px.pie(data_candidate_wise, values="% of Votes", names='Party', title="Vote Percentage", width=1000)
    st.plotly_chart(fig)
    max = data_candidate_wise['% of Votes'].max()

    st.header("Winner-")
    st.write(data_candidate_wise[data_candidate_wise['% of Votes'] == max])
    data_candidate_wise=data_candidate_wise.sort_values(by=['Total Votes'],ascending=False)
    margin = data_candidate_wise.iat[0,4]-data_candidate_wise.iat[1,4]
    st.write('Margin-',str(margin))
