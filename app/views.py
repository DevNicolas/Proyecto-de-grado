from flask import request, redirect, render_template, url_for
from app import app
import requests
from bs4 import BeautifulSoup

@app.route('/' )
def index():

    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result_search():
    query = request.form['search']
    query_search = query.replace(" ","+")
    #url = requests.get("https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q={}&btnG=&oq=".format(query_search))
    url = requests.get("https://scholar.google.com/citations?view_op=search_authors&mauthors="+query_search)
    sou = BeautifulSoup(url.content, "html.parser")
    lists = sou.find_all("div", class_="gs_ai")

    articles = []
    content = []
    for list in lists:
        title = list.find("h3").getText() #encuentra perfiles de cientificos
        universidad = list.find("div", {'class': 'gs_ai_aff'}).getText()
        cargo = list.find("div", {'class': 'gs_ai_eml'}).getText()
        url = list.find("a", href=True).attrs['href']
        #area = list.find("div", {'class': 'gs_ai_int'}).getText()
        article = title+"$"+universidad+"$"+cargo #+ "$" + content + "$" + profile + "$" + book_url + "$" + cite + "$" + url_article
        articles.append(article)
        content.append(url)

    return render_template('result_search.html', lists=articles, query=query, content = url )



@app.route('/profile', methods=["GET"])
def profile():
    complement = request.args.get('title' )

    page = requests.get("https://scholar.google.com/"+complement)
    bsObj = BeautifulSoup(page.content, "html.parser")
    perfil = bsObj.findAll("div", {"id": "gsc_prf_i"})
    contenido = bsObj.findAll("table", {"id": "gsc_a_t"})
    grafica = bsObj.findAll("div", {"class": "gsc_md_hist_b"})
    profile = []
    for info in perfil:
        nombre = info.findAll("div")
        name = nombre[0].get_text()
    profile.append(name)

    for texto in contenido:
        todo = []
        titulo = texto.findAll("tr")
        todo.append(texto.get_text())

    for indice in grafica:
        guardar = []
        cont = indice.findAll("span")
        guardar.append(indice.get_text())

    return render_template('profile.html', perfil = profile, contenido = todo, grafica = guardar)
