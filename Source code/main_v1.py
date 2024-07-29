# %%
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# %%
# Initialize the main window root as ctk
root = ctk.CTk()
# Destroy or close of window
def on_close():
    root.destroy()

# %%
# Header for requests
headers = {'User-Agent': 'Chrome/39.0.2171.95 Safari/537.36'}

# %%
# Access the page and return web response
def web_page_access1(website_url):
    web_response = requests.get(website_url, headers=headers)
    return BeautifulSoup(web_response.text, 'html.parser')

# %%
# Render the homepage and return movie list
def home_page_rendering(category_url):
    soup = web_page_access1(category_url)
    soup_list1 = soup.find_all('a')
    list_name_site = [soup_list1[i].text for i in range(len(soup_list1))]
    list_name_link = [i.get('href') for i in soup_list1]
    movie_list_dict = dict(zip(list_name_site, list_name_link))
    return movie_list_dict

# %%
# Clean the movie page, storing in dictionary and movie Choosing
def dict_cleaning(category_url):
    render_dict = home_page_rendering(category_url)
    keys_to_remove1 = ['Skip to content','New Movies','HD Movies','Dubbed Movies','Web Series','Korean Drama','TamilYogi','','\n ']
    keys_to_remove2 = list(render_dict.keys())[-3:]
    for key in list(render_dict.keys()):
        if key in keys_to_remove1 or key in keys_to_remove2:
            del render_dict[key]
    for widget in root.winfo_children():
        widget.destroy()
    
    # Movie list Lable 
    ctk.CTkLabel(root, text='Movie List: ', font=("Arial", 20)).place(relx=0.03, rely=0.03)
    
    # creating frame for movie buttons
    frame1 = ctk.CTkFrame(root, fg_color="#242424", bg_color="transparent", height=500)
    frame1.pack(side=tk.LEFT)
    frame1.place(rely=0.1, relx=0.04)

    frame2 = ctk.CTkFrame(root, fg_color="#242424", bg_color="transparent")
    frame2.pack(side=tk.LEFT)
    frame2.place(rely=0.1, relx=0.52)

    # Movie Button Creation
    keys = list(render_dict.keys())
    for i, key in enumerate(keys):
        if i % 2 == 0:
            button = ctk.CTkButton(frame1, text=key, fg_color='#242424', command=lambda key=key: choice_selection(key, render_dict[key]))
            button.pack(side=tk.TOP, anchor=tk.W)
        else:
            button = ctk.CTkButton(frame2, text=key, fg_color='#242424', command=lambda key=key: choice_selection(key, render_dict[key]))
            button.pack(side=tk.TOP, anchor=tk.W)

# %%
# Extract the streaming link using regex
def link_extraction(html_link):
    soup = web_page_access1(html_link)
    soup_list3 = soup.find_all('script')    # using BS4 to find the <Script> tag
    script_list = [str(i) for i in soup_list3]
    pattern = r'file:"(https?://[^"]+)"'    # pattern to find the link in js
    file_urls = []
    for script in script_list:
        matches = re.findall(pattern, script)
        file_urls.extend(matches)
    return file_urls

# %%
# Get movie Finding Second HTML find and links for streaming
def movie_links(movie_name):
    soup = web_page_access1(movie_name)
    soup_list2 = soup.find_all('iframe')    # using BS4 to find inside <iframe> tag
    list_name_link = [i.get('src') for i in soup_list2] #finding Second stlm file source
    last_page = link_extraction(list_name_link[0])
    list_Title = ['Streaming','Download 720 HD','Download 360 HD', 'Download 240 HD']
    last_dict = dict(zip(list_Title, last_page))    # adding the Service name and links to dict
    return last_dict

# %%
def vlc_selection(movie_url):
    try:    # this block run when vlc find on x86 files
        vlc_path = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe' # VLC media player path on X86 files
        # vlc command to the path and movie url
        vlc_command = [vlc_path, movie_url]
        subprocess.Popen(vlc_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except: # this block run when vlc find on program files
        vlc_path = r'C:\Program Files\VideoLAN\VLC\vlc.exe' # VLC media player path for Store installed file
        vlc_command = [vlc_path, movie_url]
        # below line access the subprocess to acess the vlc and streme movie
        subprocess.Popen(vlc_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# %%
# This function that helps to close the window and Streme movie on vlc
def close_and_stream(movie_url):
    vlc_selection(movie_url)
    root.destroy()
    exit()

# %%
# Display the selected movie and options
def choice_selection(movie_name, movie_page_link):
    movie_page_clean = movie_links(movie_page_link)
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(root, text='Selected Movie: ', font=("Arial", 20)).place(relx=0.13, rely=0.2)
    movie_name_print = ctk.CTkLabel(root, text=movie_name, font=("Arial", 20))
    movie_name_print.place(relx=0.25, rely=0.4)

    # placement values to for loop
    x = 0.20
    y = 0.67

    # Download button functions
    for key in movie_page_clean:
        if key != 'Streaming':
            button = ctk.CTkButton(root, text=key, command=lambda key=key: print(f'clicked {key}'))
            button.place(relx=x, rely=y)
            x += 0.2
    
    # clicking the button it close the GUI and play on vlc
    S_button = ctk.CTkButton(root, text='Close and Stream on VLC', font=("Arial", 16), command=lambda: close_and_stream(movie_page_clean['Streaming']))
    S_button.place(relx=0.38, rely=0.57)

# %%
# Search box functionality
def search_box():
    # This line for destroy the previous widgets in the window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Search lable and the search boc 
    ctk.CTkLabel(root, text="Search ", font=("Arial", 20)).place(relx=0.39, rely=0.33, anchor='center')
    text_box = ctk.CTkEntry(master=root, width=300, placeholder_text='Type the Movie Name...')
    text_box.place(relx=0.5, rely=0.4, anchor='center')

    # this function that used to create the link and access dict clean for the movie given in search box
    def search():
        search_string = text_box.get()
        search_url = f'https://tamilyogi.blog/?s={search_string}'
        dict_cleaning(search_url)

    search_button = ctk.CTkButton(root, text="Submit", command=search)
    search_button.place(relx=0.5, rely=0.5, anchor='center')

# %%
# Display category selection buttons
def user_selection():
    # Categroy selection and link in dict
    ctk.CTkLabel(root, text='Select Category given below', font=("Arial", 20)).place(relx=0.375, rely=0.5)
    category_url = {
        'New Movies': 'https://tamilyogi.blog/category/tamilyogi-full-movie-online/',
        'HD Movies': 'https://tamilyogi.blog/category/tamil-hd-movies/',
        'Dubbed Movies': 'https://tamilyogi.blog/category/tamilyogi-dubbed-movies-online/'
    }

    # x and y vaues to  for loop to print buttons
    x = 0.13
    y = 0.67

    # To add categroy Buttons
    for key in category_url:
        button = ctk.CTkButton(root, text=key, command=lambda key=key: dict_cleaning(category_url[key]))
        button.pack(side=tk.LEFT)
        button.place(relx=x, rely=y)
        x += 0.2

    # search box button
    search_button = ctk.CTkButton(root, text='Search', command=search_box)
    search_button.pack(side=tk.LEFT)
    search_button.place(relx=x, rely=y)


# %%
# Main function to start the application
def main():

    # Size of window, icon and title for GUI woindow 
    root.geometry('1070x600')
    root.iconbitmap(r"src/icon.ico")
    root.title("Watch Tamil Movie on VLC")

    # Welcome msg and start button to start the code
    ctk.CTkLabel(root, text='Welcome, press Start to Begin...', font=("Arial", 20)).place(relx=0.13, rely=0.2)
    ctk.CTkButton(root, text="Start", command=user_selection).place(relx=0.5, rely=0.4, anchor='center')

    # line 1 for the destry of window while cicking close button and next lien for running the Gui in main loop
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


# %%
if __name__ == '__main__':
    main()


