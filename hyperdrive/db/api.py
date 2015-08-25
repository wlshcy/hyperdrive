from  session import get_session
import models


def model_query(model,**kwargs):
    model = model
    session = get_session()
    with session.begin():
        query = session.query(model).filter_by(**kwargs)

    return query


def add_item(values):
    session = get_session()
    with session.begin():
        model=models.Item()
        model.update(values)
        model.save(session=session)

def get_items():
    return model_query(models.Item).\
                           order_by(models.Project.created).\
			   all()

def get_item(id):
    return model_query(models.Item,id=id).first()

def delete_item(id):
    return model_query(models.Item,id=id).delete()

def update_item():
    pass
