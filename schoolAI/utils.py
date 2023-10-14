from schoolAI import db
from openai import ChatCompletion
from schoolAI.errors.handlers import CustomError


# openai helpers
def explain(topic):
    message = [
        {
            "role": "system",
            "content": "you are a very helpful and knowledgable teacher",
        },
        {
            "role": "user",
            "content": f"Explain the following in a detailed easy-to-understand way:\n{topic}",
        },
    ]
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.5,
        max_tokens=190,
    )

    return response["choices"][0]["message"]["content"].strip("\n").strip()


# user input validation helpers
def raise_input_error(error):
    msg = ""
    for err in error.errors():
        err_name=err['loc'][0]
        message=err['msg']
        if err_name=="topics":
            message="ensure this field is a list of strings with minimum 5 characters"
        msg += f"{err_name}:{message}, "
    raise CustomError("Bad Request", 400, msg)


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
