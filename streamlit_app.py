# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your smoothie
    """
)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberry", "Peaches"),
# )

# st.write("You selected:", option)

name_on_order=st.text_input("Name on Smoothie")
st.write("Name on your Smoothie will be: ",name_on_order)
cnx=st.connection("snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()

ingredients_list=st.multiselect(
    'choose upto 5 Ingredients: '
,my_dataframe,max_selections=5)

if ingredients_list:

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen+' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        # st.text(smoothiefroot_response.json())
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +  """','"""+name_on_order+ """')"""
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert=st.button('Submit Order')
    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")



        
















