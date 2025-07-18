# === Imports ===
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# === Function to scrape data ===
def scrape_apollo(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.apollo.io/")

    time.sleep(5)  # Wait for Apollo to load

    # Try to accept cookies or login popup if shown (Optional handling)
    try:
        driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']").click()
    except:
        pass

    # Find and enter the search keyword in the search bar
    try:
        search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search by name, title, company, etc.']")
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)
    except Exception as e:
        print("Search box not found:", e)
        driver.quit()
        return

    time.sleep(5)  # Wait for search results to load

    people_cards = driver.find_elements(By.CSS_SELECTOR, ".PeopleListstyles__StyledListItem-sc-__sc-1sjp1hi-1")

    results = []

    for card in people_cards[:20]:  # Limit to first 20 results for performance
        try:
            name = card.find_element(By.CSS_SELECTOR, "a span").text
            title = card.find_element(By.CSS_SELECTOR, "p[class*='Title']").text
            company = card.find_element(By.CSS_SELECTOR, "p[class*='Company']").text
            results.append({
                "Name": name,
                "Title": title,
                "Company": company
            })
        except:
            continue

    driver.quit()

    # Save to Excel
    df = pd.DataFrame(results)
    df.to_excel("ApolloPeople.xlsx", index=False)
    print("✅ Data saved to ApolloPeople.xlsx")


# === Tkinter GUI ===
def start_gui():
    def run_scraper():
        keyword = entry.get()
        if keyword:
            scrape_apollo(keyword)
            status_label.config(text="✅ Scraping complete!")

    window = tk.Tk()
    window.title("Apollo Scraper")
    window.geometry("400x200")

    label = tk.Label(window, text="Enter keyword to search on Apollo.io:")
    label.pack(pady=10)

    entry = tk.Entry(window, width=50)
    entry.pack(pady=5)

    button = tk.Button(window, text="Scrape", command=run_scraper)
    button.pack(pady=10)

    status_label = tk.Label(window, text="")
    status_label.pack()

    window.mainloop()


# === Run the GUI ===
if __name__ == "__main__":
    start_gui()
