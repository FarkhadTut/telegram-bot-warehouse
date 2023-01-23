from database.connector import con
import pandas as pd
from math import isnan
import sys
import warnings
warnings.filterwarnings("ignore")
# poll_dict['data'][lang][i][f'answers'].append([answer, next_question, answer_id, id_source])



EMOJI = '\u2705'
NEXT_BUTTON = '\u27A1 Далее'
RETURN_BUTTON = 'Назад \u21A9'
LOCATION_BUTTON = 'Локация жўнатиш \U0001f4cd'
CONTACT_BUTTON = 'Kontakt yuborish \u1F4F2'

type_product = pd.read_sql(sql="SELECT * FROM products_type", con=con)
product = pd.read_sql(sql="SELECT * FROM products_product", con=con)
identifier = pd.read_sql(sql="SELECT * FROM products_identifier", con=con)

PRODUCT_QUESTIONS = ['Выберите тип продукта:','Выберите продукт:','Выберите идентификатор:']


poll = pd.read_sql(sql="SELECT * FROM survey_poll", con=con)
questions = pd.read_sql(sql="SELECT * FROM survey_question", con=con)
answers = pd.read_sql(sql="SELECT * FROM survey_answer", con=con)

users = pd.read_sql(sql="SELECT * FROM users_user  WHERE user_type != 'admin'", con=con)
# def check_user(chat_id):
    




def poll_to_dict(poll_, questions_, answers_, add_return_button=True):
    suka = False
    langs = ['ru', 'uz']
    poll_dicts = []
    mask = poll_['status'] == 1 #chosing active poll, can be chosen by user in the future
    active_polls = poll_[mask]
    
    for j in active_polls.index:
        poll = active_polls.iloc[j]
        active_poll_id = poll['id']
        # poll = poll_[mask]
        poll_dict = {}
        poll_dict['data'] = {}
        
        for lang in langs:
            # if lang == 'ru':
            #     continue

            poll_dict['data'][lang] = {}

            mask = questions_['poll_id'] == active_poll_id
            questions = questions_[mask]
            questions.reset_index(drop=True, inplace=True)
            questions.sort_values(by='num', inplace=True)
            for i in questions.index:
                next_question_for_database_answers = None
                poll_dict['data'][lang][i] = {}
                question = questions[lang].iloc[i]
                # if 'product_id' in questions.columns:

                num = questions['num'].iloc[i]
                question_id = questions['id'].iloc[i]
                type_ = questions['type'].iloc[i]
                finish = questions['finish'].iloc[i]
                mask = answers_['question_id'] == questions['id'].iloc[i]
                answers = answers_[mask]
                poll_dict['data'][lang][i][f'question'] = question
                poll_dict['data'][lang][i][f'num'] = num
                poll_dict['data'][lang][i][f'type'] = type_
                poll_dict['data'][lang][i][f'finish'] = finish
                poll_dict['data'][lang][i][f'question_id'] = question_id
                poll_dict['data'][lang][i][f'answers'] = []
                answers.reset_index(drop=True, inplace=True)
                id_source = None
                answers['id_source'] = [id_source] * len(answers.index)
                # if type_ == 'multiple':
                #     poll_dict['data'][lang][i][f'answers'].append([NEXT_BUTTON, next_question, 0, id_source])

                if len(answers) != 0:
                    go_out = False
                    table = 'users_user'
                    
                    
                    if answers['show_users'].values.tolist()[0] == 'show_not_confirmed_users':
                        query = f"SELECT * FROM {table} WHERE confirmed = 0 AND user_type != 'admin' AND deleted == 0"
                    elif answers['show_users'].values.tolist()[0] == 'show_confirmed_users':
                        query = f"SELECT * FROM {table} WHERE confirmed = 1 AND user_type != 'admin' AND deleted == 0"
                    elif answers['show_users'].values.tolist()[0] == 'show_all_users':
                        query = f"SELECT * FROM {table} AND deleted == 0"
                    else:
                        go_out = True

                    if not go_out:

                        answers_df = pd.read_sql(sql=query, con=con)
                        next_question = answers['next_question'].values[0]
                        answers_df['next_question'] = [None]* len(answers_df.index)
                        id_source = table
                        answers_df['id_source'] = [table] * len(answers_df.index)
                        # answers_df.drop_duplicates([lang], keep='first', inplace=True)
                        answers = answers_df
                        answers[lang] = None
                        for user in answers.index:
                            answers[lang].iloc[user] = answers['name'].iloc[user] + ' ' + answers['surname'].iloc[user]
                        
                        
                        # poll_dict['data'][lang][i][f'answers'].append([RETURN_BUTTON, next_question, -1, id_source])
                        
                if type_ == 'multiple':
                    poll_dict['data'][lang][i][f'answers'].append([NEXT_BUTTON, next_question, 0, id_source])
              
                # elif type_ == 'users':
                #     for i in users.index:
                #         mask = users['confirmed'] == 0
                #         user_id = users[mask]['id'] 
                #         id_source = 'users_user'
                #         # next_question = 
                #     poll_dict['data'][lang][i][f'answers'].append([user_id, next_question, 0, id_source])
                
                # if isinstance(answers['product'].iloc[index], str):
                #         table = answers['product'].iloc[index]
                #         query = f'SELECT * FROM {table}'
                #         answers_df = pd.read_sql(sql=query, con=con) 
                #         answers_df.drop_duplicates([lang], keep='first', inplace=True)
                #         answer = answers_df[lang]
                
                if len(answers) == 1 and 'product' in answers.columns and  answers['product'].iloc[0] != None:
                    next_question_for_database_answers = answers['next_question'].iloc[0]
                if not 'surname' in answers.columns and len(answers['product']) != 0 and isinstance(answers['product'][0], str):
                    table = answers['product'][0]
                    query = f"SELECT * FROM {table}"
                    if table =='products_type':
                        if poll['name'] == 'Sklad':
                            query = f"SELECT * FROM {table} WHERE warehouse = 'raw'"
                        elif poll['name'] == 'Ready products':
                            query = f"SELECT * FROM {table} WHERE warehouse = 'ready_prod'"
                        pass
                    answers_df = pd.read_sql(sql=query, con=con)
                    ans = answers_df[lang].values.tolist() 
                    answers_df['next_question'] = [None]* len(answers_df.index)
                    if next_question_for_database_answers != None:
                        answers_df['next_question']  = next_question_for_database_answers                    
                    id_source = table
                    answers_df['id_source'] = [table] * len(answers_df.index)
                    answers_df.drop_duplicates([lang], keep='first', inplace=True)
                    
                    answers = answers_df
                    if 'deleted' in answers_df.columns:
                        answers = answers_df[answers_df['deleted'] == 0]
                
                    
                    # answers_ = answers_df[lang].values.tolist()
                # if isinstance(answers['product']):
                #         table = answers['product'].iloc[index]
                #         query = f'SELECT * FROM {table}'
                answers.reset_index(drop=True, inplace=True)
                if j == 1 and i ==0:
                    answers = answers[answers['deleted'] == 0]
                for k, index in enumerate(answers.index):
                    answer = answers[lang].iloc[index]
                    answer_id = answers['id'].iloc[index]
                    next_question = answers['next_question'].iloc[index]
                    
                    # print(answer, next_question)
                    if next_question == None or  isnan(next_question):
                        next_question = i + 2
                    # if lang=='uz':
                    #     print(question)
                    # if k == 0 and add_return_button and i != 0:
                    #     poll_dict['data'][lang][i][f'answers'].append([RETURN_BUTTON, next_question, -1, id_source])
                        # if suka and lang =='uz':
                        #     print(k , add_return_button, i)
                        #     print(poll_dict['data'][lang][i][f'answers'])
                        #     print(question)
                        #     sys.exit()
                    poll_dict['data'][lang][i][f'answers'].append([answer, next_question, answer_id, id_source])
                 
                if i != 0:
                    poll_dict['data'][lang][i][f'answers'].append([RETURN_BUTTON, -1, -1, None])
        poll_dict['id'] = active_poll_id
        poll_dict['name'] = poll['name']
        poll_dicts.append(poll_dict)
    return poll_dicts


def get_poll_from_database(add_return_button=True):
    return poll_to_dict(poll, questions, answers, add_return_button=True)