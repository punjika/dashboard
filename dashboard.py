import streamlit as st 
import plotly.express as px 
import pandas as pd 
import os
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Social Media", page_icon=":bar_chart", layout="wide")

st.title(" :bar_chart: Social Media Trends") 
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
fl=st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df=pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\Admin\OneDrive\Desktop\coherence1.0hacks")
    df=pd.read_csv("SocialMediaUsersDataset.csv",encoding="ISO-8859-1")
    
    
col1, col2 = st.columns((2))
df["DOB"]=pd.to_datetime(df["DOB"])

#get nim amnd max
startdate = pd.to_datetime(df["DOB"]).min()
enddate = pd.to_datetime(df["DOB"]).max()    

with col1:
    date1=pd.to_datetime(st.date_input("start dob", startdate))
    
with col2:
    date2=pd.to_datetime(st.date_input("end dob", enddate))    
    
df=df[(df["DOB"] >=date1) & (df["DOB"]<date2)].copy()   
 
st.sidebar.header("choose your filter:")
Country = st.sidebar.multiselect("Pick your Country",df["Country"].unique())
if not Country:
    df2=df.copy()
else:
    df2=df[df["Country"].isin(Country)]
  
City = st.sidebar.multiselect("Pick your City",df["City"].unique())    
if not City:
    df3=df2.copy()
else:
    df3=df2[df2["City"].isin(City)]  
#create for gender    
Gender=st.sidebar.multiselect("pick Gender", df3["Gender"].unique())     
#filter the data based on country, city and gender
if not Country and not City and not Gender:
    filter_df=df
elif not City and not Gender:
    filter_df=df[df["Country"].isin(Country)]
elif not Country and not Gender:
    filter_df=df[df["City"].isin(City)]  
elif City and Gender:
    filter_df=df3[df["City"].isin(City) & df3[Gender].isin(Gender)]   
elif Country and Gender:
    filter_df=df3[df["Country"].isin(Country) & df3[Gender].isin(Gender)]        
elif Country and City:
    filter_df=df3[df["Country"].isin(Country) & df3[City].isin(City)]       
elif Gender:
    filter_df=df3[df3["Gender"].isin(Gender)]       
else:
    filter_df= df3[df3["Country"].isin(Country) & df3["City"].isin(City) & df3["Gender"].isin(Gender)]   
    
#'''Country_df = filter_df.groupby(by=["Country"], as_index=False)["Interests"]

#with col1:
 #   st.subheader("Country wise interest")
  #  fig = px.bar(Country_df, x="Country", y="Interests", text=['${:,.2f}'.format(x) for x in Country_df["Interests"]])

   # st.plotly_chart(fig,use_container_width=True,height=200)
    
#with col2:
 #   st.subheader("gender wise Interests")
  #  fig=px.pie(filter_df, values="Interests", names="Region", hole=0.5) 
   # fig.update_traces(text=filter_df[Gender], textposition="outside")
    #st.plotly_chart(fig,use_container_width=True)   '''
    

    # Display bar graph for gender distribution
with col1:    
    st.subheader("Gender Distribution")
    gender_counts = df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_gender = px.bar(gender_counts, x="Gender", y="Count", title="Gender Distribution", color="Gender")
    st.plotly_chart(fig_gender)
with col2:
    st.subheader("Country Distribution")
    Country_counts = df["Country"].value_counts().reset_index()
    Country_counts.columns = ["Country", "Count"]
    fig_Country= px.bar(Country_counts, x="Country", y="Count", title="Country Distribution", color="Country")
    st.plotly_chart(fig_Country)
       
#filter_df["month_year"]=filter_df["DOB"].dt.to_period("M")
st.subheader("Line Series Analysis")

#linechart = pd.DataFrame(filter_df.groupby(filter_df["month_year"]).dt.strftime("%y : %b"))[""]   
def preprocess_data(df):
    # Explode multivalued interests into separate rows
    df = df.explode("Interests")
    return df

# Preprocess data
df = preprocess_data(df)
df_filtered = df[df['Interests'].isin(['Movies', 'Fashion', 'Music', 'Sports'])]

# Streamlit app
def main():
    st.title('Visualizations for Columns')
    
    # Visualization 1: City-wise Distribution
    st.subheader('City-wise Distribution')
    fig_city = px.histogram(df_filtered, x='City', title='City-wise Distribution')
    st.plotly_chart(fig_city)

    # Visualization 2: Country-wise Distribution
    st.subheader('Country-wise Distribution')
    fig_country = px.histogram(df_filtered, x='Country', title='Country-wise Distribution')
    st.plotly_chart(fig_country)

    # Visualization 3: Interest-wise Distribution
    st.subheader('Interest-wise Distribution')
    fig_interest = px.histogram(df_filtered, x='Interests', title='Interest-wise Distribution')
    st.plotly_chart(fig_interest)

if __name__ == "__main__":
    main()
    

st.subheader('City-wise Distribution (Pie Chart)')


fig_city_pie = px.pie(df['City'].value_counts(), names=df['City'].value_counts().index)
fig_city_pie.update_traces(marker_colors=px.colors.qualitative.Pastel)
st.plotly_chart(fig_city_pie, use_container_width=True) 