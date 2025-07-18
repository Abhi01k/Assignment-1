# === Imports ===
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tkinter import Tk, Label, Entry, Button

# === Scraper Function ===
def scrape_amazon(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.amazon.in/")
    time.sleep(2)

    # Search for the keyword
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(keyword)
    search_box.submit()
    time.sleep(4)

    # Scroll to load more sponsored products
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    products = driver.find_elements(By.XPATH, "//div[contains(@data-component-type, 's-search-result')]")
    scraped_data = []

    for product in products:
        try:
            # Check if sponsored
            if "Sponsored" not in product.text:
                continue

            title = product.find_element(By.XPATH, ".//h2/a").text
            product_url = product.find_element(By.XPATH, ".//h2/a").get_attribute("href")

            try:
                brand = product.find_element(By.XPATH, ".//h5/span").text
            except:
                brand = "N/A"

            try:
                rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").text.split()[0]
            except:
                rating = "N/A"

            try:
                reviews = product.find_element(By.XPATH, ".//span[@class='a-size-base']").text
            except:
                reviews = "0"

            try:
                price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            except:
                price = "N/A"

            try:
                image_url = product.find_element(By.XPATH, ".//img").get_attribute("src")
            except:
                image_url = "N/A"

            scraped_data.append({
                "Title": title,
                "Brand": brand,
                "Rating": rating,
                "Reviews": reviews,
                "Price": price,
                "Image URL": image_url,
                "Product URL": product_url
            })
        except Exception as e:
            continue

    driver.quit()

    # Save to Excel
    df = pd.DataFrame(scraped_data)
    df.to_excel("Amazon_Sponsored_Products.xlsx", index=False)
    print("✅ Data saved to Excel file!")

# === GUI using Tkinter ===
def run_gui():
    def on_click():
        keyword = entry.get()
        if keyword:
            status_label.config(text="Scraping in progress...")
            root.update()
            scrape_amazon(keyword)
            status_label.config(text="✅ Done! Check Excel file.")

    root = Tk()
    root.title("Amazon Scraper")
    root.geometry("400x200")

    Label(root, text="Enter Amazon Search Keyword:", font=("Arial", 12)).pack(pady=10)
    entry = Entry(root, width=40)
    entry.pack()

    Button(root, text="Scrape Sponsored Products", command=on_click).pack(pady=10)
    status_label = Label(root, text="", font=("Arial", 10), fg="green")
    status_label.pack()

    root.mainloop()

# === Run GUI ===
if __name__ == "__main__":
    run_gui()
