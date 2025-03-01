# Import python packages
import streamlit as st
st.title('My Parents Diner')
# New Section
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie
    """)


name_on_order = st.text_input('Name on Smoothie')
st.write("The name on your Smoothie will be", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections= 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
     ingredients_string += fruit_chosen +' '
    
   # st.write(ingredients_string)

    my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submint Order')
    if time_to_insert:

       session.sql(my_insert_stmt).collect()

       st.success('Your Smoothie is ordered!', icon="✅")
