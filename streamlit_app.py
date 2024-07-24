# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose 5 ingredients:",
    my_dataframe,
    max_selections = 5
   )

if ingredients_list:   
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen+ ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_submit = st.button('Submit Order')
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

my_dataframe_order = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe_order)
time_to_insert_order=st.button('UPDATE ORDER')
#st.success("UPDATED")
if (time_to_insert_order):
    st.success('Your is order updated', icon="✅")

og_dataset = session.table("smoothies.public.orders")
edited_dataset = session.create_dataframe(editable_df)
    
# try:
#     og_dataset.merge(edited_dataset
#                              , (og_dataset['order_uid'] == edited_dataset['order_uid'])
#                              , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
        
#                         )
#     st.success('Order(s) updated', icon = '👍')
    
# except:
#         st.error('something went wrong')    
        
