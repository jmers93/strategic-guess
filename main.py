import streamlit as st
import random
import pandas as pd

st.title("Guess the number 🔢")
N_ATTEMPTS = 5
HI = 64
ID_TO_TAB = {
    "strategic": "Version 1",
    "simple": "Version 2"
}

def get_random_number(mode):
    if mode == "strategic":
        return get_strategic_random_number()
    return get_really_random_number()


def get_really_random_number():
    return random.randint(1, HI)


def get_strategic_random_number():
    out = [
        3, 6, 7, 9, 12, 13, 18, 19, 25, 28, 31, 34, 37, 38, 41, 43, 44, 
        47, 50, 56, 57, 62, 63, 67, 71, 75, 81, 82, 
        87, 88, 90, 93, 94
        ]
    out += list(range(0, HI+1, 5))
    out += list(range(0, HI+1, 2))
    possible_choices = [i for i in range(1, HI+1) if i not in out]
    return random.choice(possible_choices)


def update_results(res, tab, mode):
    if mode == "Win":
        res.loc[tab, "N Wins"] += 1
    res.loc[tab, "N Attempts"] += 1
    res.loc[tab, "% Success"] = "{:.2%}".format(res.loc[tab, "N Wins"] / res.loc[tab, "N Attempts"])


tab_strat, tab_simple, tab_stats = st.tabs(["Version 1", "Version 2", "Statistics"])

if "results" not in st.session_state:
    st.session_state["results"] = pd.DataFrame(
        index=["Version 1", "Version 2"], 
        columns=["N Wins", "N Attempts", "% Success"]
        )
    st.session_state["results"].fillna(0, inplace=True)
    st.session_state["results"]["% Success"] = "NaN"

def create_game(id):
    tab = ID_TO_TAB[id]
    key_attempts = f"number_attempts_{id}"
    key_wins = f"number_wins_{id}"
    key_secret = f"secret_{id}"
    if key_attempts not in st.session_state:
        st.session_state[key_attempts] = N_ATTEMPTS
    if key_wins not in st.session_state:
        st.session_state[key_wins] = 0
    if key_secret not in st.session_state:
        st.session_state[key_secret] = get_random_number(id) 

    random_number = st.session_state[key_secret]
    number_entered = st.number_input(
        f"Guess a number betwen 1 and {HI}", 
        min_value=1, 
        max_value=HI,
        format="%i",
        key=f"input_{id}")
    # st.write(f"Secret number {random_number}")

    if st.button("Submit Answer", key=f"submit_{id}"):
        if number_entered == random_number:
            st.session_state[key_secret] = get_random_number(id)
            st.balloons()
            st.session_state[key_wins] += 1
            st.session_state[key_attempts] = N_ATTEMPTS
            st.success("You Win! Game restarted!")
            update_results(st.session_state["results"], tab, "Win")
        elif number_entered > random_number:
            st.warning("Guess too high!")
        else:
            st.warning("Guess too low!")
        st.session_state[key_attempts] -= 1
    # Restart the game
    if st.session_state[key_attempts] == 0:
        update_results(st.session_state["results"], tab, "Lose")
        st.session_state[key_secret] = get_random_number(id)
        st.session_state[key_attempts] = N_ATTEMPTS
        st.error(f"You lost. The secret number was {random_number}. Game restarted!")
    st.write("---")
    st.write(f"Attempt Number: {N_ATTEMPTS - st.session_state[key_attempts] + 1}")
    st.write(f"Number of Attempts Left: {st.session_state[key_attempts]}")
    

with st.sidebar:
    st.write("**Created by:**")
    st.caption("Juan Montero | https://github.com/jmonteroers")

with tab_strat:
    create_game("strategic")

with tab_simple:
    create_game("simple")

with tab_stats:
    st.table(st.session_state["results"])