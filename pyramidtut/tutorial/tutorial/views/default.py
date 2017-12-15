from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError


from ..models import Post
from ..models import User

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    query = request.dbsession.query(Post,User.name).join(User, User.id==Post.creator_id)
    return dict(query =query)


@view_config(route_name ='new_user',renderer  = '../templates/new_user.jinja2')
def new_user(request):
    return {}
@view_config(route_name = 'post',renderer='../templates/post.jinja2')
def post(request):
    post = request.dbsession.query(Post).all()
    return dict(post = post)

@view_config(route_name ='add_post',renderer = '../templates/add_post.jinja2',request_method = 'POST' )
def add_post(request):
    user_id = request.params["user_id"]
    # import ipdb
    # ipdb.set_trace()
    return{ 'user_id':user_id }

@view_config(route_name = 'storepost',request_method = 'POST')
def storepost(request):
    post_name = request.params['post_name']
    post_data = request.params['textarea']
    user_id = request.params["user_id"]
    request.dbsession.add(Post(name = post_name,data = post_data,creator_id = user_id ))
    return HTTPFound(location = request.route_url('login'))

@view_config(route_name ='edit_post',renderer = '../templates/edit_post.jinja2')
def edit_post(request):
    edit_post = request.params["edit_post"]
    post = request.dbsession.query(Post).filter_by(id = edit_post).one()
    return dict(post= post)

@view_config(route_name ='update_post',request_method = 'POST')
def update_post(request):
    post_id = request.params["post_id"]
    post = request.dbsession.query(Post).filter_by(id = post_id).one()
    if 'submit' in request.params:
        post.name  = request.params['post_name']
        post.data  =  request.params['textarea']
        import transaction
        transaction.commit()
    return HTTPFound(location = request.route_url('home'))
# delete_post
@view_config(route_name ='delete_post',renderer = '../templates/mytemplate.jinja2')
def delete_post(request):
     delete_id = request.params["delete_post"]
     post = request.dbsession.query(Post).filter_by(id = delete_id).one()
     request.dbsession.delete(post)
     return HTTPFound(location = request.route_url('home'))

     