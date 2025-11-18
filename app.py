import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt






st.set_page_config(layout="wide")
# email = st.text_input("Enter email")
# password = st.text_input("Enter Password")
# gender=st.selectbox("select Gender",['male','female','others'])

# btn = st.button("Login/Signup")

# if btn:
#     if email== "roshan@gmail.com" and password =="1234":
#         st.success("login Sucessfull")
#         st.balloons()
#         st.write(gender)
#     else:
#         st.error("login fail")

df=pd.read_csv("1startup_funding.csv")

#data cleaning and pre processing
df['Investors Name']=df['Investors Name'].fillna("Undisclosed")
df.drop(columns=['Remarks'],inplace=True)
df.set_index('Sr No',inplace=True)




df.rename(columns={
    "Date dd/mm/yyyy":"date",
    "Startup Name":"startup",
    "Industry Vertical":"vertical",
    "SubVertical":"subvertical ",
    "City  Location":"city",
    "Investors Name":"investors",
    "InvestmentnType":"round",
    "Amount in USD":"amount"
},inplace = True)

df['amount']=df['amount'].fillna("0")
df['amount']=df['amount'].str.replace(',','')
df['amount']=df['amount'].str.replace('undisclosed','0')
df['amount']=df['amount'].str.replace('unknown','0')
df['amount']=df['amount'].str.replace('Undisclosed','0')
df['amount']=df['amount'].str.replace('+','')


df=df[df['amount'].str.isdigit()]
df['amount']=df['amount'].astype('float')

#doller to inr in cr
def to_inr(dollar):
    inr=dollar * 88.77
    return inr/10000000


df['amount']=df['amount'].apply(to_inr)
df['date'] = df['date'].str.replace('05/072018','05/07/2018')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df = df.dropna(subset=['startup','city','investors','round','amount'])
df['year'] = df['date'].dt.year


#clean data export
df.to_csv("starteup Cleaned.csv")

df['month']=df['date'].dt.month
df['year']=df['date'].dt.year



#functions for app
def load_investor_details(investor):
    st.title(investor)
    #load the resent 5 investments of the investor
    last_5_df=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader("Most recent 5 investments")
    st.dataframe(last_5_df)

    #biggest investments
    st.subheader("biggest investments")
    # Create two columns

    col1, col2 = st.columns(2)
    big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    # st.subheader("biggest investments")
    with col1:
        #st.dataframe(big_series)
        st.subheader("biggest investments graph")
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        st.subheader("sector invested")
        vertical_series=df[df['investors'].str.contains(investor)].groupby("vertical")['amount'].sum().head(3)
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    
    #round invested
    st.subheader("sector invested")
    col3, col4 = st.columns(2)
    with col3:
        round_series=df[df['investors'].str.contains(investor)].groupby("round")['amount'].sum().head(3)
        fig2,ax2=plt.subplots()
        ax2.pie(round_series,labels=round_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        round_series=df[df['investors'].str.contains(investor)].groupby("city")['amount'].sum().head(3)
        fig3,ax3=plt.subplots()
        ax3.pie(round_series,labels=round_series.index,autopct="%0.01f%%")
        st.pyplot(fig3)

    #yearOnYear investments
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig4,ax4=plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.subheader("yearly investments")
    st.pyplot(fig4)
#load overall analysis
def load_overall_analysis():
    col1,col2,col3,col4=st.columns(4)
    st.title("Overall Analysis")
    #total invested amount
    total=round(df['amount'].sum())
    #max
    max=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #average
    avrage_funding=df.groupby('startup')['amount'].sum().mean()
    #total funded startup
    num_startups=df['startup'].nunique()

    with col1:
        st.metric("Total Investments(Cr)",total)
    with col2:
        st.metric("Max Investments(Cr)",max)
    with col3:
        st.metric("Average Investments(Cr)",round(avrage_funding))
    with col4:
        st.metric("Total Funded Startups",num_startups)
    

    st.header("MOM graph")
    selected_option=st.selectbox("select type",["Total","Count"])
    if selected_option=="Total":
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()
    
    temp_df['x_axis']=temp_df['month'].astype('str') + "-" +temp_df['year'].astype('str')

    fig3,ax3=plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)

def funding_type_analysis(df):
    st.subheader("Type of Funding Analysis")

    round_df = df.groupby('round')['amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.bar(round_df.index, round_df.values)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Pie chart for share
    fig1, ax1 = plt.subplots()
    ax1.pie(round_df, labels=round_df.index, autopct="%0.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

def city_wise_funding(df):
    st.subheader("City-wise Funding Distribution")

    city_df = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.bar(city_df.index, city_df.values)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)



def top_startups_analysis(df):
    st.subheader("Top Funded Startups - Yearly & Overall")

    # Overall
    top_overall = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
    st.write("**Overall Top Startups**")
    st.dataframe(top_overall)

    # Year-wise breakdown
    years = sorted(df['year'].dropna().unique().tolist())
    selected_year = st.selectbox("Select Year", years)
    top_year = (
        df[df['year'] == selected_year]
        .groupby('startup')['amount']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots()
    ax.bar(top_year.index, top_year.values)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


def top_investors(df):
    st.subheader("Top Investors by Total Investment")

    investor_series = (
        df.assign(investors=df['investors'].str.split(','))
          .explode('investors')
          .groupby('investors')['amount']
          .sum()
          .sort_values(ascending=False)
          .head(10)
    )

    fig, ax = plt.subplots()
    ax.bar(investor_series.index, investor_series.values)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
import seaborn as sns

def funding_heatmap(df):
    st.subheader("Funding Heatmap (Year vs Month)")

    heatmap_df = df.groupby(['year', 'month'])['amount'].sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_df, annot=False, fmt=".0f", cmap="YlGnBu", ax=ax)
    st.pyplot(fig)















st.sidebar.title("startup funding analysis")

option=st.sidebar.selectbox("select one",['Overall Analysis',"StartUP","Investor"])

# if option== "Overall Analysis":
#      st.title("Overll Analysis")
#      btn0 = st.sidebar.button("Show overall Analysis")
#      if btn0:
#         load_overall_analysis()

if option == "Overall Analysis":
    st.title("Overall Analysis")

    if "show_overall" not in st.session_state:
        st.session_state.show_overall = False

    if st.sidebar.button("Show Overall Analysis"):
        st.session_state.show_overall = True

    if st.session_state.show_overall:
        load_overall_analysis()

        st.markdown("funding type analysis")
        funding_type_analysis(df)

        st.markdown("city wise funding")
        city_wise_funding(df)

        st.markdown("top startups analysis")
        top_startups_analysis(df)

        st.markdown("top investors analysis")
        top_investors(df)

        st.markdown("funding heatmap")
        funding_heatmap(df)
        
    else:
        st.info("👈 Click **'Show Overall Analysis'** on the sidebar to view the full analytics.")



elif option == "StartUP":
    selected_startup = st.sidebar.selectbox("Select Startup", sorted(df['startup'].unique().tolist()))

    if "show_startup" not in st.session_state:
        st.session_state.show_startup = False

    if st.sidebar.button("Find Startup"):
        st.session_state.show_startup = True

    if st.session_state.show_startup:
        st.title(f"Startup Analysis: {selected_startup}")
        
        startup_df = df[df['startup'] == selected_startup].sort_values('date', ascending=False)
        
        st.subheader("Startup Details")
        st.dataframe(startup_df[['date','vertical','subvertical ','city','round','investors','amount']])
        
        st.subheader("Funding Over Time")
        fig, ax = plt.subplots()
        ax.plot(startup_df['date'], startup_df['amount'])
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount (Cr)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.subheader("Funding by Round")
        round_series = startup_df.groupby('round')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.bar(round_series.index, round_series.values)
        plt.xticks(rotation=45)
        st.pyplot(fig1)


else:
    selected_investor=st.sidebar.selectbox("select investors",sorted(set(df['investors'].str.split(",").sum())))
    btn2=st.sidebar.button("find investor")
    st.title("Investors analysis")
    if btn2:
        load_investor_details(selected_investor)

    # st.title("Investors analysis")

