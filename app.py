import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import utils
import json
from aggregation import get_games_guesses_duels_dataframes, create_duel_guesses_google_map

st.title('GeoCoach')
st.write('''
GeoCoach is a one-stop shop for improving your GeoGuessr performance and visualizing your gameplay at scale.
It surfaces insights that aren't possible in GeoGuessr's Game Breakdowns & Recaps, and generates 
interactive maps showing you how you've explored the world and what you've learned over time. Identify
your weaknesses & strengths, or just stop by to enjoy your unique data visualized!''')
st.divider()

ncfa_guide_url = 'https://github.com/SafwanSipai/geo-insight?tab=readme-ov-file#getting-your-_ncfa-cookie'

ncfa = st.text_input('Enter your NCFA cookie ([click here to obtain yours](%s))' % ncfa_guide_url, None)
if ncfa:
    with st.spinner(text='Fetching data...'):
        session = utils.get_session(ncfa)
        game_tokens = utils.get_game_tokens(session)

    default_number_of_games = 100 if len(game_tokens) > 100 else len(game_tokens)
    st.slider('How many games would you like to analyze? (400 games ~ 1 min analysis time)', 0, len(game_tokens), default_number_of_games,
              step=10, key='slider', 
              help='''Adjusting the slider value determines the number of your most recent games to analyze. 
                      For instance, selecting '50' will analyze your fifty most recent games. 
                      Please note that higher values will increase processing time accordingly.''')
    
    button = st.button('Analyze')
    
    if button:
        progress_bar = st.progress(0)
        stats = utils.get_stats(session, game_tokens, st.session_state.slider, progress_bar)
        mov_stats = stats['moving']
        no_mov_stats = stats['no-moving']
        nmpz_stats = stats['nmpz']

        # Store game_tokens in session state AFTER analysis
        st.session_state.game_tokens = game_tokens



        def plot_and_display_data(stats, label):
            
            #st.text(json.dumps(stats, indent=4)) #Display the entire stats dictionary in Streamlit

            # Extracting most and least stats for points and distances per country
            most_pts, least_pts = utils.get_most_and_least_data_avg(stats, type='points')
            most_dist, least_dist = utils.get_most_and_least_data_avg(stats, type='distance')

            # Plotting figures
            points_vs_time_fig = utils.plot_points_vs_time(stats)
            points_hist_fig = utils.points_histogram(stats)
            countries_bar_fig = utils.plot_countries_bar_chart(stats)
            #guessed_loc_fig = utils.plot_guessed_locations(stats['guessed_locations'])
            # Add my new plots here
            #guessed_loc_fig_2 = utils.plot_guessed_locations_2(stats['guessed_locations'])
            #round_loc_fig = utils.plot_round_locations(stats['round_locations'])
            round_and_guess_fig = utils.plot_round_and_guessed_locations(stats['round_locations'], stats['guessed_locations'])
            # After getting the stats
            interactive_map = utils.create_interactive_map(stats['round_locations'], stats['guessed_locations'])

            # Displaying data and figures in the corresponding tab
            with label:
                col1, col2 = st.columns(2)
                col1.metric('Total Games', str(stats['number_of_games']))
                col2.metric('Total Rounds', str(stats['number_of_rounds']))

                col1, col2, col3 = st.columns(3)
                col1.metric('Average Points', str(stats['average_score']))
                col2.metric('Average Distance', str(stats['average_distance']) + ' KM')
                col3.metric('Average Game Time', str(stats['average_time']) + ' seconds')

                st.write('Points lost per country - Least vs Most')
                col1, col2 = st.columns(2)
                col1.dataframe(least_pts[::-1], hide_index=True)
                col2.dataframe(most_pts, hide_index=True)

                st.write('Distance per country - Least vs Most')
                col1, col2 = st.columns(2)
                col1.dataframe(least_dist[::-1], hide_index=True)
                col2.dataframe(most_dist, hide_index=True)

                st.pyplot(countries_bar_fig)
                st.pyplot(points_vs_time_fig)
                st.pyplot(points_hist_fig)
                #st.pyplot(guessed_loc_fig)
                # Add my new plot here
                #st.pyplot(guessed_loc_fig_2)
                #st.pyplot(round_loc_fig)
                st.pyplot(round_and_guess_fig)
                # Display the map in Streamlit
                st.components.v1.html(interactive_map._repr_html_(), width=1000, height=800)


        progress_bar.empty()
        
        st.header('Singleplayer Games')
        mov, no_mov, nmpz = st.tabs(['Moving', 'No moving', 'NMPZ'])
        
        plot_and_display_data(mov_stats, mov)
        plot_and_display_data(no_mov_stats, no_mov)
        plot_and_display_data(nmpz_stats, nmpz)

    standard_games, standard_guesses, duel_games, duel_tokens, duel_guesses = get_games_guesses_duels_dataframes()
    st.header("Standard Games")
    st.dataframe(standard_games, use_container_width=True)
    st.header("Standard Guesses")
    st.dataframe(standard_guesses, use_container_width=True)
    st.header("Duel Games")
    st.dataframe(duel_games, use_container_width=True)
    st.header("Duel Guesses")
    st.dataframe(duel_guesses, use_container_width=True)


    # Create the map
    create_duel_guesses_google_map(duel_guesses)
    
    # In your Streamlit app:
    st.title("Duel Guesses Map")
    # Display the map in Streamlit using components.html
    st.components.v1.html(open("duel_guesses_google_map.html").read(), height=600)

    # JSON printing (separate button, always visible) - commented out for now
#    if st.button("Print Game JSON (Caution: Large Output)"):
#        if 'game_tokens' in st.session_state:
#            game_index = st.number_input("Enter the index of the game to print (0-based)", min_value=0, max_value=len(st.session_state.game_tokens) - 1, value=0)
#            try:
#               game_token = st.session_state.game_tokens[game_index]
#                game_data = session.get(f"{utils.BASE_URL_V3}/games/{game_token}").json()
#                st.write(json.dumps(game_data, indent=4))  # json is now available
#            except Exception as e:
#                st.error(f"Error fetching or displaying JSON: {e}")
#        else:
#            st.error("Please click 'Analyze' first to fetch game data.")