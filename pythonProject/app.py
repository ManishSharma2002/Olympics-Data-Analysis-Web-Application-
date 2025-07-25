import streamlit as st
import pandas as pd
import preprocessor ,helper
import matplotlib.pyplot as plt
import seaborn as sns
import  plotly.express as px
import plotly.figure_factory as ff


region_df = pd.read_csv("noc_regions.csv")
df= pd.read_csv("athlete_events.csv")

st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

st.sidebar.title("Olympic Analysis")
df =preprocessor.preprocess(df,region_df)
user_menu = st.sidebar.radio(
    "select an option",
    ("Medal Tally","Overall Analysis","Country-wise Analysis","Athlete wise Analysis")
)
if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally= helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympic")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " Overall Performance")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympic")

    st.table(medal_tally)

if user_menu == "Overall Analysis":
    edition = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sport = df["Sport"].unique().shape
    event = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape
    nation = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sport)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(event)
    with col2:
        st.header("Nations")
        st.title(nation)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nation_over_time = helper.data_over_time(df,"region")
    fig = px.line(nation_over_time, x="Edition", y="region")
    st.title("Participating Nation over the year")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, "Event")
    fig = px.line(event_over_time, x="Edition", y="Event")
    st.title("Event over the year")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the year")
    st.plotly_chart(fig)

    st.title("No of Event over time(Event sport)")
    fig,ax = plt.subplots(figsize= (20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax= sns.heatmap(x.pivot_table(index= "Sport", columns = "Year",values = "Event",aggfunc = "count").fillna(0).astype("int"),annot = True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    selected_sport = st.selectbox("Select a Sport" , sport_list)
    x= helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")
    country_list=  df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select the country", country_list)


    country_df = helper.yearwise_tally(df,selected_country)
    fig = px.line(country_df,x= "Year",y = "Medal")
    st.title(selected_country + " Medal Tally over the year")
    st.plotly_chart(fig)


    st.title(selected_country + " Excel in the followiing sports")
    pt = helper.country_event_heaatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    if not pt.empty:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    else:
        st.write("No medal data available for " + selected_country)
    # ax = sns.heatmap(pt, annot=True)
    # st.pyplot(fig)

    st.title("Top 10 athletes of " +selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == "Athlete wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize = False,width  = 1000,height = 600)
    st.title("Distribution Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    st.title("Height vs Weight")
    selected_sport = st.selectbox("Select a Sport ", sport_list)
    temp_df = helper.weight_v_height_df(df ,selected_sport)
    fig , ax = plt.subplots()
    ax= sns.scatterplot(x= temp_df["Weight"], y= temp_df["Height"], hue = temp_df["Medal"],style = temp_df["Sex"],s =60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig= px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)






