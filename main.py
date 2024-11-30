import streamlit as st
import requests

# Replace with your OMDb API key
api_key = "c64a9236"

# Placeholder image URL for missing posters
placeholder_img = "https://via.placeholder.com/250x375.png?text=No+Poster+Available"


def fetch_movie_details(movie_name_):
    """
    Fetch movie details from the OMDb API.
    """
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name_}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        movie_details_ = {
            "Title": data.get("Title"),
            "Year": data.get("Year"),
            "Genre": data.get("Genre"),
            "Director": data.get("Director"),
            "Actors": data.get("Actors"),
            "Plot": data.get("Plot"),
            "Poster": data.get("Poster"),
            "Metascore": data.get("Metascore"),
            "Country": data.get("Country"),
            "Runtime": data.get("Runtime"),
            "imdbRating": data.get("imdbRating"),  # Get IMDb rating for the main movie
        }
        return movie_details_
    else:
        return None


def fetch_recommendations(movie_name_):
    """
    Fetch recommended movies based on Genre, Director, or Actors.
    """
    url = f"http://www.omdbapi.com/?apikey={api_key}&s={movie_name_}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        recommendations_ = []
        for item in data.get("Search", [])[:5]:  # Limit to 5 recommendations
            recommendations_.append({
                "Title": item.get("Title"),
                "Year": item.get("Year"),
                "Poster": item.get("Poster"),
                "imdbRating": item.get("imdbRating"),  # Get IMDb rating for recommended movies
            })
        return recommendations_
    else:
        return []


# Streamlit App
# Apply CSS to customize interface color (Lighter theme)
st.markdown(
    """
    <style>
    /* Global background color for the whole page */
    body {
        background-color: #f4f4f9;  /* Light gray background */
        color: #333333;  /* Dark text color for readability */
        font-family: 'Arial', sans-serif;
    }

    /* Header and Title Styling */
    h1 {
        color: #2c3e50;  /* Dark blue color for main title */
        font-size: 3rem;
    }

    h2 {
        color: #2c3e50;  /* Dark color for subtitles */
        font-size: 2rem;
    }

    h3 {
        color: #34495e;  /* Slightly lighter color for smaller headings */
    }

    /* Customize input fields (search bar) */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 1px solid #ccc;
        color: #333;
    }

    /* Customize buttons */
    .stButton>button {
        background-color: #3498db;  /* Light blue button */
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #2980b9;  /* Darker blue on hover */
    }

    /* Customize the image display */
    .stImage img {
        border-radius: 8px;
        margin-top: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Customize the sidebar background */
    .css-1d391kg {
        background-color: #3498db;
    }

    /* Change the color of the plot or description text */
    p, .stText {
        font-family: 'Arial', sans-serif;
        color: #333;
    }

    /* Adjusting input field borders and labels */
    .stTextInput label {
        color: #2c3e50;
    }

    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Movie Explorer")

# Search bar for movie input
movie_name = st.text_input("Search for a movie", "")

if movie_name:
    # Fetch details for the main movie
    movie_details = fetch_movie_details(movie_name)

    if movie_details:
        # Main Movie Information
        st.subheader(f"{movie_details['Title']} ({movie_details['Year']})")
        st.text(f"Genre: {movie_details['Genre']}")
        st.text(f"Director: {movie_details['Director']}")
        st.text(f"Actors: {movie_details['Actors']}")
        st.text(f"Runtime: {movie_details['Runtime']}")
        st.text(f"Country: {movie_details['Country']}")
        st.text(f"Metascore: {movie_details['Metascore']}")
        st.text(f"IMDb Rating: {movie_details['imdbRating']}")
        st.text_area("Plot", movie_details["Plot"], height=100)

        # Display Main Movie Poster (with check for "N/A")
        if movie_details["Poster"] and movie_details["Poster"] != "N/A":
            st.image(movie_details["Poster"], width=250)  # Reduced poster size
        else:
            st.image(placeholder_img, width=250)  # Placeholder if no poster available

        # Fetch and Display Recommended Movies
        st.subheader("Recommended Movies")
        recommendations = fetch_recommendations(movie_details["Title"])

        if recommendations:
            cols = st.columns(5)  # Create columns for recommended movies
            for col, movie in zip(cols, recommendations):
                with col:
                    # Check if the poster is valid
                    if movie["Poster"] and movie["Poster"] != "N/A":
                        st.image(movie["Poster"], use_container_width=True)
                    else:
                        st.image(placeholder_img, use_container_width=True)  # Placeholder for missing posters

                    st.caption(f"{movie['Title']} ({movie['Year']})")
                    st.text(f"IMDb Rating: {movie['imdbRating']}")
        else:
            st.text("No recommendations found.")
    else:
        st.error("Movie not found! Please try searching for another movie.")
