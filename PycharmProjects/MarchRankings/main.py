import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

def fetch_ap_poll_data(url):
    try:
        tables = pd.read_html(url)
        ap_poll_table = tables[0]
        ap_poll_table.set_index("Rk", inplace=True)

        team_names = ap_poll_table['School'].tolist()

        return team_names

    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_team_player_data(team_name):
    try:
        team_url = f'https://www.sports-reference.com/cbb/schools/{team_name.lower().replace(" ", "-")}/men/2024.html#per_game'
        response = requests.get(team_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        div_element = soup.find('div', {'id': 'switcher_per_game_players'})
        if div_element:
            table = div_element.find('table')
            if table:
                table_html = StringIO(table.prettify())
                player_data_table = pd.read_html(table_html)[0]
                player_data_table.insert(0, 'Team', team_name)  # Insert the team name as the first column
                return player_data_table
            else:
                print(f'No table found within the div on {team_name} webpage.')
                return None
        else:
            print(f'Div with ID "switcher_per_game_players" not found on {team_name} webpage.')
            return None

    except Exception as e:
        print(f"Error fetching data for {team_name}: {e}")
        return None

def main():
    url_ap_poll = 'https://www.sports-reference.com/cbb/seasons/men/2024-polls.html#current-poll'
    team_names = fetch_ap_poll_data(url_ap_poll)

    all_player_data = pd.DataFrame()  # Initialize an empty DataFrame to store all player data

    if team_names:
        for team_name in team_names:
            player_data = fetch_team_player_data(team_name)
            if player_data is not None:
                all_player_data = pd.concat([all_player_data, player_data], ignore_index=True)  # Concatenate the data

    all_player_data.to_excel('all_player_data.xlsx', index=False)  # Write the combined data to an Excel file
    print("Player data for all teams has been exported to all_player_data.xlsx")

if __name__ == "__main__":
    main()

