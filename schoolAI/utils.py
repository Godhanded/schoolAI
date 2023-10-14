from schoolAI import db
from openai import ChatCompletion


# openai helpers
def explain(topic):
    message=[{"role":"system","content":"you are a very helpful and knowledgable teacher"},{"role":"user","content":f"Explain the following in a detailed easy-to-understand way:\n{topic}"}]
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.5,
        max_tokens=160,
    )

    return response.choices[0].text.strip()


# db helpers


def query_paginated(table, page):
    return db.paginate(
        db.select(table).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )


def query_paginate_filtered(table, page, **kwargs):
    return db.paginate(
        db.select(table).filter_by(**kwargs).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )
