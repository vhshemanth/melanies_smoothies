# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in custom Smoothie!")

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name of Smoothie")
st.write("The name of your smoothie is : ", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
ingredients_list = st.multiselect('Chose upto 5 Ingredeints', my_dataframe, max_selections = 5)


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_choosen=''
    for fruit_chosen in ingredients_list:
        ingredients_choosen += fruit_chosen  + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrional Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        
        #st.text(smoothiefroot_response.json())
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_choosen)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_choosen + """' , '""" + name_on_order + """')"""

    submit = st.button("Submit Order")
    
    #st.write(my_insert_stmt)
    #st.stop()
    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")
