

import streamlit as st
import pickle
from poi_trialmerged import FINAL
import pandas as pd
from streamlit_folium import folium_static
import folium

# CSS style for a yellow and orange theme with gradients and image zoom effect
streamlit_style = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lato:wght@100;300;400;700&display=swap');

  body {
    font-family: 'Lato', sans-serif;
    background: linear-gradient(135deg, #FFDD00, #FF7F50);
    color: #333;
  }

  .main-header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background: linear-gradient(135deg, #FFDD00, #FFA500);
    border-radius: 10px;
  }

  .main-header img {
    width: 100px;
    height: auto;
    margin: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .main-header img:hover {
    transform: scale(1.2);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .hotel-bold {
    font-weight: 700;
    color: #FF4500;
  }

  .hotel-font {
    font-size: 20px;
    background-color: #FFF5E1;
    padding: 10px;
    border-radius: 5px;
  }

  label.css-1p2iens.effi0qh3, p, li {
    font-size: 18px;
    line-height: 1.6;
  }

  button.css-135zi6y.edgvbvh9 {
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(135deg, #FFA500, #FF4500);
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }

  button.css-135zi6y.edgvbvh9:hover {
    background: linear-gradient(135deg, #FF4500, #FFA500);
  }

  .image-caption {
    font-size: 14px;
    color: #333;
    text-align: center;
    margin-top: 5px;
  }

  @media only screen and (max-width: 768px) {
    .main-header img {
      width: 70px;
    }
  }

  @media only screen and (max-width: 480px) {
    .main-header img {
      width: 50px;
    }
    label.css-1p2iens.effi0qh3, p, li {
      font-size: 14px;
    }
    button.css-135zi6y.edgvbvh9 {
      font-size: 14px;
    }
  }
</style>
"""
st.markdown(streamlit_style, unsafe_allow_html=True)

# Create a responsive header section with a horizontal layout
st.markdown("## Travel Destination Highlights")

# Use Streamlit's st.image function to properly display images from the data folder
image_names = [
    "Albert Hall Museum",
    "Bapu Bajar",
    "Chokhi dani",
    "Galtaji Temple Jaipur",
    "Hawa Mahal",
    "Jaigarh Fort Jaipur",
    "Jaipur City Palace",
    "Jaipur-Zoo-1",
    "Jal Mahal",
    "Jantar Mantar Jaipur",
    "Nahargarh-Fort"
]

# Updated paths based on your folder structure
image_paths = [
    "data/Tourist-location/Albert Hall Museum.jpg",
    "data/Tourist-location/Bapu Bajar.jpeg",
    "data/Tourist-location/Chokhi dani.jpg",
    "data/Tourist-location/Galtaji Temple Jaipur.jpg",
    "data/Tourist-location/Hawa Mahal.jpg",
    "data/Tourist-location/Jaigarh Fort Jaipur.jpg",
    "data/Tourist-location/Jaipur City Palace.jpg",
    "data/Tourist-location/Jaipur-Zoo-1.jpg",
    "data/Tourist-location/Jal Mahal.jpg",
    "data/Tourist-location/Jantar Mantar Jaipur.jpg",
    "data/Tourist-location/Nahargarh-Fort.jpg"
]

# Split the images into two rows for better layout
rows = [image_paths[:6], image_paths[6:]]
row_names = [image_names[:6], image_names[6:]]

# Display images in a horizontal layout using columns and provide clickable Google search links
for row_idx, row in enumerate(rows):
    columns = st.columns(len(row))
    for idx, col in enumerate(columns):
        image_name = row_names[row_idx][idx]
        search_query = image_name.replace(" ", "+")  # Format the query for Google search
        google_search_url = f"https://www.google.com/search?q={search_query}"

        with col:
            try:
                # Display each image as a clickable link and ensure the caption is clickable as well
                col.markdown(f'<a href="{google_search_url}" target="_blank">', unsafe_allow_html=True)
                col.image(row[idx], caption="", use_column_width=True)
                col.markdown(f'<p class="image-caption"><a href="{google_search_url}" target="_blank">{image_name}</a></p>', unsafe_allow_html=True)
                col.markdown("</a>", unsafe_allow_html=True)
            except:
                col.write(f"Image {idx + 1} not found")

# Main content below the header
st.image('./data/Cover-Img.png')
st.title('Personalised Travel Recommendation and Planner')

# Load data with updated caching method
@st.cache_data
def get_data():
    return []

pickle_in = open("lol.pkl", "rb")
load_lol = pickle.load(pickle_in)

def welcome():
    return "Welcome All"

def output_main(Type, Duration, Budget, TYPE, Ques):
    output, info, map = FINAL(Type, Duration, Budget, TYPE, Ques)
    print(output)
    return [output, info, map]

def main():
    lis1 = ['Adventure and Outdoors', 'Spiritual', 'City Life', 'Cultural', 'Relaxing']
    lis2 = ['Family', 'Friends', 'Individual']

    Type = st.multiselect("Vacation type according to priority:", lis1)
    Duration = st.slider("Duration (days)", min_value=1, max_value=40)
    Duration = int(Duration)

    Budget = st.slider("Budget (INR)", min_value=200, max_value=150000, step=500)
    Budget = int(Budget)

    col1, col2 = st.columns(2)

    TYPE = col1.selectbox("Who are you travelling with?", lis2)
    Ques = col2.radio("Is covering maximum places a priority?", ['Yes', "No"])

    cutoff = Budget / Duration

    result = ""
    st.write(' ')
    if st.button("What do you recommend?"):

        try:
            RESULT = output_main(Type, Duration, Budget, TYPE, Ques)
        except:
            if cutoff < 260:
                st.subheader("Irrational. Try increasing your Budget or scaling down the Duration")
            else:
                st.subheader("Irrational. Please check your Inputs")
            return

        get_data().append({"Type": Type, "Duration": Duration,
                           "Budget": Budget, "TYPE": TYPE, "Ques": Ques})

        FINAL_DATA = pd.DataFrame(get_data())
        FINAL_DATA.to_csv('data/FinalData.csv')

        Output = RESULT[0]
        Info = RESULT[1]
        Map = RESULT[2]

        st.subheader('Your Inputs')
        st.write('{}'.format(Info[0]))
        col3, col4 = st.columns(2)
        for i in range(1, len(Info) - 5):
            try: 
                col3.write('{}'.format(Info[i]))
            except:
                continue
        for i in range(4, len(Info) - 2):
            try: 
                col4.write('{}'.format(Info[i]))
            except:
                continue
        st.write('{}'.format(Info[-2]))

        st.header('Suggested Itinerary')
        st.markdown('<p class="hotel-font"><span class="hotel-bold">Suggested Hotel/Accommodation:</span> {}<p>'.format(Info[-1]), unsafe_allow_html=True)
        st.write(' ')
        for i in range(0, len(Output)):
            st.write('{}'.format(Output[i]))

        folium_static(Map)

if __name__ == '__main__':
    main()
