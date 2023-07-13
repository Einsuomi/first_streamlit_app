import streamlit
import pandas as pd
import requests
import snowflake.connector  
from urllib.error import URLError

streamlit.title('My Parents New Health Dinner')



streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.

streamlit.dataframe(fruits_to_show)



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

streamlit.header("Fruityvice Fruit Advice!")
# streamlit.text(fruityvice_response.json())

# make the data normalized to a table
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# show the data
streamlit.dataframe(fruityvice_normalized)


# new section to display fruityvice API response

streamlit.header('Fruityvice Fruit Advice')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()



# do not run anything below 
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


# streamlit.header('What friut would you like to add')
add_my_fruit = streamlit.text_input('What friut would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('from streamlit')")

