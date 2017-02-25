from bottle import route, run, template, static_file, request
import random
import json
import pymysql
# connection to the db server has to be on top and accure only once.

user_id = 0
life = 0
coins = 0
current_adv_id = 0  # the general adv - doesnt matter now at all
chosen_option_id = 0
last_stage_id = 0
next_stage = 0

db = pymysql.connect(
    host='sql6.freesqldatabase.com',
    user='sql6159603',
    password='ISK4JfmVq9',
    charset='UTF8',
    db='sql6159603',
    cursorclass=pymysql.cursors.DictCursor)


@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    username = request.POST.get("user")
    current_adv_id = request.POST.get("adventure_id")
    with db.cursor() as cursor1:
        cursor1.execute('SELECT * FROM users WHERE name ="{}"'.format(username))
        result = cursor1.fetchall()
        print('user is new or not? :', result)
        if result:
            current_story_id = result[0]['current_step']
            life = result[0]['life']
            coins = result[0]['coins']
            user_id = result[0]['id']
        else:
            current_story_id = 1
            coins = 10
            life = 10
            cursor1.execute('INSERT INTO users (name, life, coins, current_step) VALUES ("{}", {}, {}, {})'\
            .format(username, life, coins, current_story_id))
            db.commit()
    #c1 = db.cursor()  # use WITH function inorder to keep memory clean
    with db.cursor() as c1:
        c1.execute('SELECT * from options where q_id = "{}"'.format(current_story_id))
        result1 = c1.fetchall()
        print('options are: ', result1)
        next_steps_results = [
            {"id": 1, "option_text": result1[0]['option_text']},
            {"id": 2, "option_text": result1[1]['option_text']},
            {"id": 3, "option_text": result1[2]['option_text']},
            {"id": 4, "option_text": result1[3]['option_text']}
            ]
        c1.execute('SELECT * FROM questions WHERE id = {}'.format(current_story_id))
        text = c1.fetchall()
        c1.execute('SELECT * FROM users WHERE name = "{}"'.format(username))
        result2 = c1.fetchall()
        user_id = result2[0]['id']
        user_name = result2[0]['name']
        current_adv_id = 0 #todo: if have time add new adventure - dont
    return json.dumps({"user": user_id,
                       "name": user_name,
                       "adventure": current_adv_id,
                       "last_stage": current_story_id,
                       "text": text[0]['text'],
                       "image": "wakeup.jpg",
                       "options": next_steps_results,
                       "life": life,
                       "coins": coins
                       })



@route("/story", method="POST")
def story():
    user_name = request.POST.get("name")
    last_stage_id = request.POST.get("last_stage")
    current_stage = request.POST.get("next_stage")
    print('last stage id:', last_stage_id)
    life = int(request.POST.get("life"))
    user_id = request.POST.get("user")
    current_adv_id = int(request.POST.get("adventure"))
    chosen_option_id = request.POST.get("option_chosen") #this is what the user chose - use it!
    coins = int(request.POST.get("coins"))
    print('user chose option', chosen_option_id)
    print('LAST STAGE:', last_stage_id)
    with db.cursor() as c2:
        c2.execute('SELECT * FROM options WHERE option_id = {} AND q_id = {}'.format(chosen_option_id, last_stage_id))
        query_result = c2.fetchall()
        print('THE LAST OPTION TEXT WAS:', query_result[0]['option_text'])
        try:
            choice_life = int(query_result[0]['life'])
        except:
            choice_life = 0
        try:
            choice_coins += int(query_result[0]['coins'])
        except:
            choice_coins = 0
        life += choice_life
        coins += choice_coins
        next_stage = query_result[0]['next_story_id']
        c2.execute('SELECT * FROM options WHERE q_id = {}'.format(next_stage))
        update_query = c2.fetchall()
        last_stage_id = update_query[0]['q_id']
        print(last_stage_id)
        c2.execute('SELECT * FROM options WHERE q_id = {}'.format(next_stage))
        next_question_text = c2.fetchall()
        print('NEXT QUESTION TEXT1:', next_question_text[0]['option_text'])
        print('NEXT QUESTION TEXT2:', next_question_text[1]['option_text'])
        print('NEXT QUESTION TEXT3:', next_question_text[2]['option_text'])
        print('NEXT QUESTION TEXT4:', next_question_text[3]['option_text'])
        if next_question_text:
            next_steps_results = [
                {"id": 1, "option_text": next_question_text[0]['option_text']},
                {"id": 2, "option_text": next_question_text[1]['option_text']},
                {"id": 3, "option_text": next_question_text[2]['option_text']},
                {"id": 4, "option_text": next_question_text[3]['option_text']}
                ]
        else:
            next_steps_results = [
                {"id": 1, "option_text": " "},
                {"id": 2, "option_text": " "},
                {"id": 3, "option_text": " "},
                {"id": 4, "option_text": " "}
            ]

        c2.execute('SELECT * FROM questions WHERE id = {}'.format(next_stage))
        result = c2.fetchall()

        # c2.execute('SELECT * FROM users WHERE name = "{}"'.format(username))
        # result2 = c2.fetchall()
        # user_name = result2[0]['name']

    return json.dumps({"user": user_id,
        "name": user_name,
        "adventure": current_adv_id, #the general adv - doesnt matter now at all
        "text": result[0]['text'],
        "image": result[0]['image'],
        "options": next_steps_results,
        "life": life,
        "coins": coins,
        "last_stage": last_stage_id,
        "next_stage": next_stage
        })


@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):

    return static_file(filename, root='images')

def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()

