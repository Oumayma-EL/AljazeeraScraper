import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# The lxml_parser function
def lxml_parser(link):
    html_status = requests.get(link)
    # print(html_status)
    html_text = html_status.text
    soup = BeautifulSoup(html_text, 'lxml')
    return soup


# Testing the lxml_parser function
# new_link=lxml_parser("https://www.aljazeera.com/news/2022/12/3/more-than-2-4-million-people-attended-group-stages-matches-fifa")
# print(new_link.prettify())
# Testing was fine!!
# home_link = "https://www.aljazeera.com" # The last part of the link must be without / otherwise the links will contain //
def extract_categories_and_links(home_link):
    soup = lxml_parser(home_link)

    allCategories = soup.find("ul", class_="menu header-menu")
    # print(allCategories.prettify())
    # news = allCategories.find("li", class_="menu__item menu__item--aje menu__item--has-submenu")
    # Now iterating and taking cases where the link is already there or just parsed .
    # print("List of news Menu with links:")
    otherCategories = allCategories.find_all("li", class_="menu__item menu__item--aje")
    categories_and_links = {}
    for i in otherCategories:
        cat = i.a.span.text
        link = i.a['href'].split(".")
        if "aljazeera" in link:
            cat_link = i.a['href']
        else:
            cat_link = home_link + i.a["href"]
        categories_and_links[cat] = cat_link
    return categories_and_links


# Testing the extract_categories_and_links
# categories_and_links=extract_categories_and_links(home_link)
# print(categories_and_links)
# Testing was fine

def extract_links_from_link_category(main_link, category_link):
    # main_link = "https://www.aljazeera.com"
    # category_link = "https://www.aljazeera.com/economy/"

    number_of_clicks = 150

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options, executable_path="D:\chromedriver.exe")
    driver.get(category_link)
    while number_of_clicks > 0:
        try:
            driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//button[.//span[text()='Show more']]"))))
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Show more']]"))))
            print("Show More button clicked", number_of_clicks)

        except:
            print("No more Show More button")
            break
        finally:
            number_of_clicks -= 1
    feed_section = driver.find_element(by=By.ID, value="news-feed-container")
    links = feed_section.find_elements(by=By.XPATH, value="(//a[@class='u-clickable-card__link'])")
    print(len(links))
    links_from_link_category = {}
    list_of_links = []
    for link in links:
        l = link.get_attribute("href")
        list_of_links.append(l)
        # print("####################################################")
    links_from_link_category[category_link] = list_of_links
    return links_from_link_category

    # print(link_content.prettify())


# Testing the  extract_links_from_link_category()

# links_from_link_category=extract_links_from_link_category("https://www.aljazeera.com","https://www.aljazeera.com/climate-crisis")
# print(links_from_link_category)
# This is also working !!!!!

def extract_titles_and_articles(link):
    titles_and_articles = {}
    soup = lxml_parser(link)
    try:
        main_content = soup.find("main", id="main-content-area")

        # print("\033[35mArticle title\033[0m")
        article_title = main_content.find("h1").text
        # print(article_title)
        # print("###########")
        # print("\033[35mArticle Content\033[0m")

        article_content = main_content.find_all("p")
        text = ""
        for content in article_content:
            text = text + content.text
            # print(text)
        titles_and_articles[article_title] = text
        return titles_and_articles
    except AttributeError:
        return None

    # print(main_content.prettify())


# Testing the extract_titles_and_articles :
# titles_and_articles=extract_titles_and_articles('https://www.aljazeera.com/news/2022/12/1/icj-declines-to-issue-decision-in-chile-bolivia-river-dispute')
# print(titles_and_articles)
# Testing was fine


def pick_categories(main_link, number_of_categories: int):
    assert isinstance(number_of_categories, int) == True, "Number of categories must be an integer"
    categories_and_links = extract_categories_and_links(main_link)
    all_categories = []
    categories_picked = []
    for key, value in categories_and_links.items():
        all_categories.append(key)
    while number_of_categories > 0:
        print("Pick One Category from the list below :\n", all_categories)
        category_picked = input("> ")
        if category_picked.title() in all_categories:
            categories_picked.append(category_picked.title())
            all_categories.remove(category_picked.title())
        else:
            print("Try Again:")
            continue

        number_of_categories -= 1
    return categories_picked


# Testing the function :

# categories_picked=pick_categories("https://www.aljazeera.com",3)
# print(categories_picked)

def aggregate_all(main_link, number_of_categories: int):
    categories_picked = pick_categories(main_link, number_of_categories)
    categories_and_links = extract_categories_and_links(main_link)
    new_cat_with_link = {}  # pick only the categories chosen with the link of the category
    for key, value in categories_and_links.items():
        if key in categories_picked:
            new_cat_with_link[key] = value
        continue  # continue in looping
    # print("Dictionary filtered: ", new_cat_with_link)
    # print("#####################################################################")
    cat_with_links = {}  # make a dictionary full of the category as the key and all the links to the specified articles
    for category, category_link in new_cat_with_link.items():
        links_from_link_category = extract_links_from_link_category(main_link, category_link).get(category_link)
        # print(links_from_link_category)
        cat_with_links[category] = links_from_link_category
    # pprint(cat_with_links)
    # print("#####################################################################")
    cat_with_content = {}  # make a dictionary full of the category as the key and all the content of the articles
    for cat, list_of_links in cat_with_links.items():
        list_of_content = []
        for url in list_of_links:
            titles_and_articles = extract_titles_and_articles(url)
            if titles_and_articles is None:
                continue
            list_of_content.append(titles_and_articles)
        cat_with_content[cat] = list_of_content  # list of dictionaries where the title is the key and the text is the value

    list_for_csv = []
    for category_name, category_contents in cat_with_content.items():

        for category_content in category_contents:
            short_list = []
            short_list.append(category_name)
            for k, val in category_content.items():
                short_list.append(k)
                short_list.append(val)

            list_for_csv.append(short_list)

    # print(list_for_csv)
    # weird_literal = 'þ'
    # weird_name = '\N{LATIN SMALL LETTER THORN}'
    # weird_char = '\xfe'  # hex representation
    # True
    # new_data = [[sample[0], sample[1],sample[2].replace('\n', weird_char) + weird_char]
    #             for sample in list_for_csv]
    df = pd.DataFrame(list_for_csv, columns=['category', 'title', 'article_content'])
    df.loc[:, "article_content"] = df["article_content"].apply(lambda x: x.replace('\n', '\\n'))
    df.to_csv("tech.csv", index=False, encoding='utf-8')
    


aggregate_all("https://www.aljazeera.com", 1)
