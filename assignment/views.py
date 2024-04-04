from django.shortcuts import render,HttpResponse, redirect
import random
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

nextId=4
topics = [
    {'id':1, 'title':'파스타 만드는 법', 'body':'끓는 물에 소금을 넣고 파스타 면을 삶아 알덴테 상태로 만듭니다. 별도의 팬에서 올리브 오일, 다진 마늘(또는 양파), 토마토 소스(또는 크림 소스)를 사용해 소스를 준비합니다. 삶은 파스타를 소스와 섞어 볶은 후, 원하는 토핑을 추가해 제공합니다.', 'created': datetime.now()},
    {'id':2, 'title':'간장계란밥 만드는 법', 'body':'계란 1개를 볼에 깨뜨려 넣고, 소금과 후추로 간을 한 후 잘 풀어줍니다. 팬에 식용유를 두르고 계란물을 부어 스크램블 형태로 부드럽게 볶은 다음, 밥을 추가하여 고루 섞어 볶습니다. 간장과 설탕(또는 미림)을 적당량 넣고 잘 섞어 볶은 후, 기호에 따라 참기름을 몇 방울 떨어뜨려 마무리합니다.','created': datetime.now()},
    {'id':3, 'title':'햄버거 만드는 법', 'body':'햄버거 패티는 소금과 후추로 간을 한 다음, 중간 불에서 양면을 골고루 굽습니다. 햄버거 빵은 반으로 잘라 버터를 발라 팬이나 오븐에서 살짝 구워 줍니다. 구운 빵의 아래쪽에 잎채소, 패티, 치즈, 양파, 토마토, 소스(케첩, 마요네즈 등)를 차례로 올린 후 빵 윗면을 덮어 완성합니다.','created': datetime.now()},
]

def HTMLTemplate(articleTag,id=None):
    global topics
    contextUI=''
    if id != None:
        contextUI=f'''
          <li>
            <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}>
                <input type="submit" value="삭제">  
            </form>
          </li>
          <li><a href="/update/{id}">수정</a></li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">자취생 요리 커뮤니티</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <li><a href="/create/">글쓰기</a></li>
            {contextUI}
        </ul>
    </body>
    </html>             
    '''

def index(request):
    article='''
    <h2>환영합니다</h2>
    자취생을 위한 요리 커뮤니티입니다
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            created_str = topic['created'].strftime("%Y-%m-%d %H:%M") 
            article = f'''
                <h2>{topic["title"]}</h2>
                <p>{topic["body"]}</p>
                <p>작성 시간: {created_str}</p>
            '''
            break 
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    global nextId, topics
    if request.method == 'GET':
        article='''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="제목"></p>
                <p><textarea name="body" placeholder="내용"></textarea></p>
                <p><input type="submit" value="글쓰기"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title=request.POST['title']
        body=request.POST['body']
        newTopic={"id":nextId, "title":title, "body":body, "created": datetime.now() }
        topics.append(newTopic)
        url='/read/'+str(nextId)
        nextId=nextId+1
        return redirect(url)
    
@csrf_exempt
def update(request,id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id']==int(id):
                selectedTopic= {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article=f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article,id))
    elif request.method == 'POST':
        title= request.POST['title']
        body=request.POST['body']
        for topic in topics:
            if topic['id']==int(id):
                topic['title']=title
                topic['body']=body
        return redirect(f'/read/{id}')
    
@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id=request.POST['id']
        newTopics=[]
        for topic in topics:
            if topic['id'] !=int(id):
                newTopics.append(topic)
        topics=newTopics
        return redirect('/')