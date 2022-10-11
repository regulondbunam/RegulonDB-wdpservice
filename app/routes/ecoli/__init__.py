import re
from flask import Flask, request, render_template, make_response, send_from_directory
from app.processes.ecoli.gene import Gene_collection

def collection_list(collection_name,gql_service):
    template = "no collection support"
    header_animation = True
    if collection_name == "gene":
        if request.method == 'POST':
            if request.form.get('search') == 'search':
                keyword = request.form['keyword']
                collection = Gene_collection(gql_service)
                results = collection.search(keyword)
                header_animation = False
                template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result=keyword, header_animation=header_animation)
            elif request.form.get('nextPage') == 'nextPage':
                page_current = int(request.form['current_page'])
                page_last = int(request.form['last_page'])
                if page_current<page_last:
                    page_current = page_current+1
                collection = Gene_collection(gql_service)
                results = collection.search("RDBECOLI",page_current)
                header_animation = False
                template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result="", header_animation=header_animation)
            elif request.form.get('prevPage') == 'prevPage':
                page_current = int(request.form['current_page'])
                if page_current > 0:
                    page_current = page_current-1
                collection = Gene_collection(gql_service)
                results = collection.search("RDBECOLI",page_current)
                header_animation = False
                template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result="", header_animation=header_animation)
            else:
                template = "invalid access"
        else:
            collection = Gene_collection(gql_service)
            results = collection.search("RDBECOLI")
            template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result="", header_animation=header_animation)
    return template