from pyramid.httpexceptions import HTTPFound
from pyramid.security import( remember,forget)
from pyramid.view import(forbidden_view_config,view_config)
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from ..models import User
from ..models import Post

@view_config(route_name = 'store_new_user')
def store_new_user(request):
    UserName = request.params['UserName']
    PassWord = request.params['PassWord']
    request.dbsession.add(User(name = UserName,password_hash = PassWord))
    return HTTPFound(location = request.route_url('home'))
@view_config(route_name = 'login_form', renderer = '../templates/login.jinja2')
def login_form(request):
    return {}

@view_config(route_name = 'login',renderer='../templates/post.jinja2' ,request_method = 'POST')
def login(request):
    session = request.session 
    UserName = request.params["UserName"]
    PassWord = request.params["PassWord"]
    cradentials = request.dbsession.query(User).filter_by(name = UserName).first()
    post = request.dbsession.query(Post).filter_by(creator_id = cradentials.id).all()
    if cradentials.name == UserName  and cradentials.password_hash == PassWord:
        session['current_user'] = { 'username': UserName }
        return dict(UserName = cradentials.name  , user_id =  cradentials.id,post = post)
    else:
        return render_to_response('../templates/login.jinja2',{'msg':'invalid User','UserName' : UserName,'PassWord' : PassWord,'User_name':cradentials.name,'PassWord':cradentials.password_hash},request  = request)

@view_config(route_name='logout')
def logout(request):
    session=request.session 
    headers=forget(request)
    session.invalidate()
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)