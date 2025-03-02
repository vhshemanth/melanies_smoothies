# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders")
st.write("Orders thats needs to be filled!")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submit = st.button("Submit")
    if submit:
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                         )
            st.success("Someone clicked the button", icon = "👍" )
        except:
            st.write("Something went wrong")
else:
   st.success("No pending orders", icon = "👍" ) 
