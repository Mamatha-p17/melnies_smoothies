import streamlit as st

##from snowflake.snowpark.context import get_active_session -> removinf for SNiS

from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")

st.write(
    "Choose the fruits you want in customized smoothie"
)

# option = st.selectbox(
#     "Fruits to be included in smoothie ?",
#     ("Mango", "Water melon", "Avacado"))

# st.write("Your favorite fruit is :", option)

name_on_order=st.text_input('Name on Smoothie')
st.write('Name on your smoothie : ' +name_on_order)

cnx=st.connection("snowflake")
###session = get_active_session() -> SNiS
session =cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
     'choose up to 5 Ingredients : ', my_dataframe
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''

    for each_fruit in ingredients_list:
        ingredients_string +=each_fruit +" "

    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert=st.button('SUBMIT ORDER')

    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
