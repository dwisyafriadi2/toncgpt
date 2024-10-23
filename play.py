import requests
import webbrowser
import time

def authenticate(query_data):
    """Authenticate and get the access token."""
    auth_url = "https://tapapi.chaingpt.org/authenticate"
    auth_payload = {"initData": query_data}
    auth_headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://play.tap.chaingpt.org",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    response = requests.post(auth_url, headers=auth_headers, json=auth_payload)
    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        if access_token:
            print("Authentication successful.")
            return access_token
    print("Authentication failed.")
    return None

def fetch_tasks(headers, query_data):
    """Fetch the list of tasks. Re-authenticate if the token is invalid."""
    tasks_url = "https://tapapi.chaingpt.org/tasks/all"
    response = requests.get(tasks_url, headers=headers)
    if response.status_code == 401:  # Token is invalid, re-authenticate
        print("Token is invalid. Re-authenticating...")
        new_token = authenticate(query_data)
        if new_token:
            headers["authorization"] = f"Bearer {new_token}"
            response = requests.get(tasks_url, headers=headers)  # Retry with new token
        else:
            print("Re-authentication failed.")
            return []

    if response.status_code == 200:
        return response.json().get("tasks", [])
    print("Failed to fetch tasks.")
    return []

def claim_task(headers, task_id, query_data):
    """Claim a specific task. Re-authenticate if the token is invalid."""
    claim_url = f"https://tapapi.chaingpt.org/task/claim/{task_id}"
    response = requests.post(claim_url, headers=headers)
    if response.status_code == 401:  # Token is invalid, re-authenticate
        print("Token is invalid. Re-authenticating...")
        new_token = authenticate(query_data)
        if new_token:
            headers["authorization"] = f"Bearer {new_token}"
            response = requests.post(claim_url, headers=headers)  # Retry with new token
        else:
            print("Re-authentication failed.")
            return

    if response.status_code == 200:
        print(f"Task {task_id} claimed successfully.")
    else:
        print(f"Failed to claim task {task_id}.")

def tap_screen(headers, points, taps, is_turbo_mode, query_data):
    """Tap the screen. Re-authenticate if the token is invalid."""
    tap_url = "https://tapapi.chaingpt.org/tap"
    tap_payload = {"points": points, "taps": taps, "isTurboMode": is_turbo_mode}
    response = requests.post(tap_url, headers=headers, json=tap_payload)
    if response.status_code == 401:  # Token is invalid, re-authenticate
        print("Token is invalid. Re-authenticating...")
        new_token = authenticate(query_data)
        if new_token:
            headers["authorization"] = f"Bearer {new_token}"
            response = requests.post(tap_url, headers=headers, json=tap_payload)  # Retry with new token
        else:
            print("Re-authentication failed.")
            return

    if response.status_code == 200:
        print("Tap successful:", response.json())
    else:
        print("Failed to tap.")

def auto_buy_cards(headers, query_data):
    """Automatically buy cards with 'unlocked' status. Re-authenticate if the token is invalid."""
    cards_url = "https://tapapi.chaingpt.org/cards"
    response = requests.get(cards_url, headers=headers)
    if response.status_code == 401:  # Token is invalid, re-authenticate
        print("Token is invalid. Re-authenticating...")
        new_token = authenticate(query_data)
        if new_token:
            headers["authorization"] = f"Bearer {new_token}"
            response = requests.get(cards_url, headers=headers)  # Retry with new token
        else:
            print("Re-authentication failed.")
            return

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            if card["status"] == "unlocked":
                card_id = card["id"]
                buy_url = f"https://tapapi.chaingpt.org/cards/buy/{card_id}"
                buy_response = requests.post(buy_url, headers=headers)
                if buy_response.status_code == 401:  # Token is invalid, re-authenticate
                    print("Token is invalid. Re-authenticating...")
                    new_token = authenticate(query_data)
                    if new_token:
                        headers["authorization"] = f"Bearer {new_token}"
                        buy_response = requests.post(buy_url, headers=headers)  # Retry with new token
                    else:
                        print("Re-authentication failed.")
                        return

                if buy_response.status_code == 200:
                    print(f"Card '{card['name']}' (ID: {card_id}) bought successfully.")
                else:
                    print(f"Failed to buy card '{card['name']}' (ID: {card_id}).")
    else:
        print("Failed to fetch cards.")

def daily_checkin(headers, query_data):
    """Perform daily check-in to collect rewards. Re-authenticate if the token is invalid."""
    checkin_url = "https://tapapi.chaingpt.org/collectDailyRewards"
    response = requests.post(checkin_url, headers=headers)
    if response.status_code == 401:  # Token is invalid, re-authenticate
        print("Token is invalid. Re-authenticating...")
        new_token = authenticate(query_data)
        if new_token:
            headers["authorization"] = f"Bearer {new_token}"
            response = requests.post(checkin_url, headers=headers)  # Retry with new token
        else:
            print("Re-authentication failed.")
            return

    if response.status_code == 200:
        print("Daily check-in successful:", response.json())
        print("=========================================")
        print("Join Telegram Channel")
        print("https://t.me/dasarpemulung")
    else:
        print("Failed to perform daily check-in.")

def main():
    # Read multiple queries from a file
    with open("queries.txt", "r") as file:
        queries = [line.strip() for line in file if line.strip()]

    # Ask user for actions once
    auto_tap = input("Enable auto taptap? y/n (default is n): ").strip().lower() == 'y'
    clear_tasks = input("Enable Clear task? y/n (default is n): ").strip().lower() == 'y'
    auto_buy = input("Enable Auto Buy Cards? y/n (default is n): ").strip().lower() == 'y'
    daily_check = input("Enable Daily Check-In? y/n (default is n): ").strip().lower() == 'y'

    # Repeat the process indefinitely until the user terminates the program
    while True:
        # Process each query
        for query_data in queries:
            print(f"\nProcessing query: {query_data}")

            # Authenticate and get access token
            access_token = authenticate(query_data)
            if not access_token:
                continue  # Skip to the next query if authentication fails

            # Set up headers with the access token
            headers = {
                "accept": "application/json, text/plain, */*",
                "authorization": f"Bearer {access_token}",
                "origin": "https://play.tap.chaingpt.org",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
            }

            # Execute actions based on user input
            if auto_tap:
                tap_screen(headers, points=15, taps=15, is_turbo_mode=False, query_data=query_data)

            if clear_tasks:
                tasks = fetch_tasks(headers, query_data=query_data)
                if tasks:
                    for task in tasks:
                        if task["status"] == "Pending":
                            claim_task(headers, task["id"], query_data=query_data)
                            task_link = task.get("link")
                            if task_link:
                                print(f"Opening link for task {task['id']}: {task_link}")
                                print("=========================================")
                                print("Join Telegram Channel")
                                print("https://t.me/dasarpemulung")
                                webbrowser.open(task_link)

            if auto_buy:
                auto_buy_cards(headers, query_data=query_data)

            if daily_check:
                daily_checkin(headers, query_data=query_data)

        # Indicate completion of one iteration
        print("\nCompleted one iteration of all queries.")
        print("=========================================")
        print("Join Telegram Channel")
        print("https://t.me/dasarpemulung")
        print("=========================================")
        # The loop will continue until interrupted manually by the user
        print("Repeating the process. Press Ctrl+C to stop.")
        print("Waiting Cooldown 30 Minutes")
        time.sleep(1800)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess terminated by user.")
