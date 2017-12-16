# send "one to one" notification to certain subscriber
'''response = ses.send_email(
    Source="maggiezhaomajoreee@gmail.com",
    Destination={
        'ToAddresses': ["rz2390@columbia.edu"]
    },
    Message={
        'Subject': {
            'Data': "test1",
            'Charset': 'UTF-8'
        },
        'Body': {
            'Text': {
                'Data': "test1111",
                'Charset': 'UTF-8'
            }
        }
    }
)'''

# send notification to all subscribers
'''response = sns.publish(
    TopicArn='arn:aws:sns:us-east-1:055370712479:SignUpNoti',
    Message='you have just created an event',
    Subject='event notification',
)'''

import boto3
sns = boto3.client(
    'sns',
    aws_access_key_id='AKIAJJYDESANU5YJLSNQ',
    aws_secret_access_key='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',
    # aws_session_token=SESSION_TOKEN,
)
ses = boto3.client(
    'sns',
    aws_access_key_id='AKIAJJYDESANU5YJLSNQ',
    aws_secret_access_key='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',
    # aws_session_token=SESSION_TOKEN,
)

import pymongo
import datetime
client = pymongo.MongoClient('ec2-54-172-172-28.compute-1.amazonaws.com', 27017)
#client = pymongo.MongoClient('localhost', 27017)
db1 = client.user
db2 = client.event
User= db1.user
Event= db2.event
ID= 0
EID= 0

def create_student(info):
    global ID
    ID = ID + 1
    dic = {
        'id': ID,
        'nick_name': info['nick_name'],
        'avatar': info['avatar'],
        'email': info['email'],
        'password': info['password'],
        'followings': None,
        'introduction': info['introduction'],
        'create_event': None,
        'join_event': None,
        'followers':None
    }
    User.insert(dic)

    #subscribe to our web application
    response1 = sns.subscribe(
        TopicArn='arn:aws:sns:us-east-1:055370712479:SignUpNoti',
        Protocol='email',
        Endpoint=dic['email']
    )
    print("sns",response1,"sns")

    #verify ses service
    response2 = ses.verify_email_address(
        EmailAddress=dic['email']
    )
    print("ses", response2, "ses")

    return ID

def create_event_db(info, user_id):
    global EID
    EID = EID + 1
    d= datetime.datetime.now()
    dic = {
        'id': EID,
        #'event_id':info['event_id'],
        'image': info['image'],
        'starter': user_id,
        'type':info['type'],
        'content':info['content'],
        'person_limit':30,
        'start_year': 2017,
        'start_month': 7,
        'start_day': 31,
        'start_hour': 11,
        'end_year': 2018,
        'end_month': 12,
        'end_day': 31,
        'end_hour': 12,
        'time_limit_flag':False,
        'person_limit_flag':False,
        'follower': None,
        'joined_flag':False
    }
    Event.insert(dic)
    return dic, EID


def find_student(id):
    info= User.find_one({"id": id})
    return info

def find_name_student(name):
    info = User.find_one({"nick_name": name})
    return info

def get_event_from_db():
    d = datetime.datetime.now()
    for c in Event.find():
        if(c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
            print(c)
            c['time_limit_flag'] = True
    content= Event.find({'person_limit_flag': False, 'time_limit_flag': False})
    return content

def all_study_event():
    d = datetime.datetime.now()
    for c in Event.find():
        if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
            print(c)
            c['time_limit_flag'] = True
    context= Event.find({"type": 'study', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def all_eat_event():
    d = datetime.datetime.now()
    for c in Event.find():
        if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
            print(c)
            c['time_limit_flag'] = True
    context = Event.find({"type": 'eat', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def all_home_event():
    d = datetime.datetime.now()
    for c in Event.find():
        if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
            print(c)
            c['time_limit_flag'] = True
    context = Event.find({"type": 'home', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def find_my_moment(info):
    follower= info['followers']
    return follower

def get_all_my_event(user_id):
    context= Event.find({'starter': user_id})
    return context

