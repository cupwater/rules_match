import pandas as pd
from bs4 import BeautifulSoup

def remove_html_tag(source_page):
    content = ''
    html_content_soup = BeautifulSoup(source_page) 
    title_list = html_content_soup.find_all('title')
    for title_node in title_list:
        content += title_node.get_text()
    p_list = html_content_soup.find_all('p', attrs={'class':None})
    for p_node in p_list:
        content += p_node.get_text()
    code_list = html_content_soup.find_all('code')
    for code_node in code_list:
        content += code_node.get_text()
    li_list = html_content_soup.find_all('li', attrs={'id':None, 'class':None, 'a':None})
    for li_node in li_list:
        content += li_node.get_text()
    em_list = html_content_soup.find_all('em')
    for em_node in em_list:
        content += em_node.get_text()
    strong_list = html_content_soup.find_all('strong')
    for strong_node in strong_list:
        content += strong_node.get_text()
    return content

path = r'auto_storage_class.csv'
column_names = ['ID', 'Description', 'URL', 'Source_Page']

csv_data = pd.read_csv(path)
csv_data.head()
csv_data.columns = ['Id', 'Description', 'Url', 'Source_page']
# print(csv_data.head())


for source_page in csv_data['Source_page']:
    if not isinstance(source_page, str):
        continue
    content = remove_html_tag(source_page)
    with open("%s.txt" % (fname.split(".")[0] + str(index)),"w") as f:
        f.write(content)
    with open("%s.lab" % (fname.split(".")[0] + str(index)),"w") as f:
        f.write(fname)

# Iterate over given columns only from the dataframe
# for source_page_index in range(len(csv_data['Source_page'])):
    # content = remove_html_tag(csv_data['Source_page'][source_page_index])