# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in custom Smoothie!")

cnx = st.connection("snowfalke")
session = cnx.session()

name_on_order = st.text_input("Name of Smoothie")
st.write("The name of your smoothie is : ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Chose upto 5 Ingredeints', my_dataframe, max_selections = 5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_choosen=''
    for fruit_chosen in ingredients_list:
        ingredients_choosen += fruit_chosen  + ' '
    #st.write(ingredients_choosen)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_choosen + """' , '""" + name_on_order + """')"""

    submit = st.button("Sumbit Order")
    
    #st.write(my_insert_stmt)
    #st.stop()
    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")
