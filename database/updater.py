from math import prod
from numpy import record
from database.connector import con
import pandas as pd
import sqlite3
from datetime import datetime 
from uuid import uuid4
from utils.utils import transform_to_users_df, generate_report
import sys


def convert_to_df(results):
    columns= ['answer_id', 'question_id', 'answer_type', 'answer_id_source', 'record_id']
    record_df = pd.DataFrame(columns=columns)
    record_dict = dict.fromkeys(columns)
    record_id = str(uuid4())
    responses = results['responses']
    for i, r in enumerate(responses):
        id_source = r[-1]
        if id_source  == 'survey_openanswer':
            open_asnwer_dict = {}
            open_asnwer_dict['answer'] = r[0][0]
            open_asnwer_dict['question_id'] = r[1]
            cursor=con.cursor()
            cursor.execute('INSERT INTO survey_openanswer (answer, question_id) VALUES (?,?)',  (open_asnwer_dict['answer'], int(open_asnwer_dict['question_id'])))
            con.commit()
            answer_id = cursor.lastrowid
            r[0] = [answer_id]

        for mult_choice in r[0]:
            record_dict['answer_id'] = mult_choice
            record_dict['question_id'] = r[1]
            record_dict['answer_type'] = r[2]
            record_dict['answer_id_source'] = r[3]       
            record_df = record_df.append(record_dict,  ignore_index=True)
    # record_df['date'] = pd.to_datetime(record_df.date, format='%Y-%m-%d %H:%M')
    record_df['date'] = datetime.now()
    record_df['user_id'] = results['user_id']
    record_df['poll_id'] = results['poll_id']
    record_df['record_id'] = record_id
    return record_df

def upload_results(results):
    record_df = convert_to_df(results)
    user_id = results['user_id']
    record_df.to_sql(con=con, name='survey_response', if_exists='append', index=False)
    report_df = generate_report(record_df)
    report_df.reset_index(drop=True, inplace=True)
    return report_df


def register_user(results):
    record_df = convert_to_df(results)
    user_id = results['user_id']
    users_df = transform_to_users_df(record_df, user_id)
    
    for col in users_df.columns:
        print(users_df[col])
    users_df.to_sql(con=con, name='users_user', if_exists='append', index=False)


def admin_update(results, success):
    record_df = convert_to_df(results)
    user_id = results['user_id']    
    cursor = con.cursor()
    print(record_df)
    if 65 in record_df['question_id'].values.tolist() and success:# and 'success' in record_df['answer_type'].iloc[-1]:
        answer_ids = []
        mask = record_df['question_id'] == 65
        start_idx = record_df[mask].index.values[0]
        record_df = record_df.iloc[start_idx:].reset_index(drop=True)
        for idx in record_df['answer_id'].index:
            print(idx)
            question_id = record_df['question_id'].iloc[0]
            query = f'''SELECT num FROM survey_question WHERE id={question_id}'''
            cursor.execute(query)
            question_num = cursor.fetchall()[0][0] + 1
            answer_id_source = record_df['answer_id_source'].iloc[idx]
            answer_id = record_df['answer_id'].iloc[idx]
            query = f'''SELECT * FROM {answer_id_source} WHERE id={answer_id}'''
            cursor.execute(query)
            answers = cursor.fetchall()
            print(answer_id_source)
            if answer_id_source == 'survey_openanswer':
                if idx == 0:
                    dict_product = {}
                    dict_product['uz'] = answers[0][-1]
                else:
                    dict_product['ru'] = answers[0][-1]
            if answer_id_source == 'products_type':
                type_id = record_df['answer_id'].iloc[idx]
                dict_product['type_id'] = type_id
                df_product = pd.DataFrame()
                df_product.append(dict_product, ignore_index=True)
                cursor.execute(f'SELECT max(id) FROM products_product')
                max_id = cursor.fetchone()[0]
                id = 0
                if max_id != None:
                    id = max_id +1
                query = f'''INSERT INTO products_product VALUES (?, ?, ?, ?, ?)'''
                dict_product["deleted"] = 0
                cursor.execute(query, (id, dict_product['ru'], dict_product['uz'], type_id, dict_product["deleted"]))
                product_id = cursor.lastrowid
                con.commit()
                print(f'INSERTED PRODUCT {dict_product["uz"]}')
            
            if answer_id_source == 'products_identifier':
                cursor.execute(f'SELECT max(id) FROM products_identifier')
                max_id = cursor.fetchone()[0]
                id = 0
                if max_id != None:
                    id = max_id +1
                print(answers)
                dict_identifier = {}
                dict_identifier['id'] = id
                dict_identifier['ru'] = answers[0][1]
                dict_identifier['uz'] = answers[0][2]
                query = f'''INSERT INTO products_identifier VALUES (?, ?, ?, ?)'''
                cursor.execute(query, (id, dict_identifier['ru'], dict_identifier['uz'], product_id))
                con.commit()

    elif 77 in record_df['question_id'].values.tolist() and success:# and 'success' in record_df['answer_type'].iloc[-1]:
        answer_ids = []
        mask = record_df['question_id'] == 77
        start_idx = record_df[mask].index.values[0]
        record_df = record_df.iloc[start_idx:].reset_index(drop=True)
        dict_identifier = {}
        for idx in record_df['answer_id'].index:
            print(record_df)
            question_id = record_df['question_id'].iloc[0]
            query = f'''SELECT num FROM survey_question WHERE id={question_id}'''
            cursor.execute(query)
            question_num = cursor.fetchall()[0][0] + 1
            answer_id_source = record_df['answer_id_source'].iloc[idx]
            answer_id = record_df['answer_id'].iloc[idx]
            query = f'''SELECT * FROM {answer_id_source} WHERE id={answer_id}'''
            cursor.execute(query)
            answers = cursor.fetchall()
            if answer_id_source == 'survey_openanswer':
                if idx == 0:
                    dict_identifier = {}
                    dict_identifier['uz'] = answers[0][-1]
                else:
                    dict_identifier['ru'] = answers[0][-1]

            if 'uz' in dict_identifier.keys() and 'ru' in dict_identifier.keys():
                cursor.execute(f'SELECT max(id) FROM products_identifier')
                max_id = cursor.fetchone()[0]
                id = 0
                if max_id != None:
                    id = max_id + 1

                answer_id = record_df[record_df['answer_type'] == 'single' ]['answer_id'].values[0]
                answer_id_source = record_df[record_df['answer_type'] == 'single' ]['answer_id_source'].values[0]
                dict_identifier['id'] = id
                dict_identifier['deleted'] = 0
                query = f'''INSERT INTO products_identifier VALUES (?, ?, ?, ?, ?)'''
                cursor.execute(query, (id, dict_identifier['ru'], dict_identifier['uz'], answer_id, dict_identifier['deleted']))
                con.commit()
                break
        
    elif 89 in record_df['question_id'].values.tolist() and success:# and 'success' in record_df['answer_type'].iloc[-1]:
        product_identifier_id = record_df['answer_id'].values[-2]
        table = record_df['answer_id_source'].values[-2]
        # query = f'''DELETE FROM {table} WHERE id={product_identifier_id}''' 
        query = f'''UPDATE products_identifier SET deleted =1 WHERE id = {product_identifier_id}'''
        cursor.execute(query)
        con.commit()  
    elif 87 in record_df['question_id'].values.tolist() and success:
        product_type = {}
        for idx in record_df.index:
            if record_df['answer_id_source'].iloc[idx] == 'survey_openanswer':
                question_id = record_df['question_id'].iloc[idx]
                query = f"""SELECT answer FROM survey_openanswer WHERE question_id = {question_id}"""
                cur = con.cursor()
                cur.execute(query)
                answer = [a[0] for a in cur.fetchall()]
                answer = answer[-1]
                if not 'uz' in product_type.keys():
                    product_type['uz'] = answer 
                elif not 'ru' in product_type.keys():
                    product_type['ru'] = answer

                # print(product_type)
        product_type['poll_id'] = 5
        deleted = 0
        product_type['warehouse'] = 'raw'
        if 114 in record_df['answer_id'].values:
            product_type['warehouse'] = 'ready_prod'
        query = """INSERT INTO products_type (uz, ru, poll_id, deleted, warehouse) VALUES (?,?,?,?,?)"""
        cur.execute(query, (product_type['uz'], product_type['ru'], product_type['poll_id'], deleted, product_type['warehouse']))
        con.commit()
    
    elif 90 in record_df['question_id'].values.tolist() and success:# and 'success' in record_df['answer_type'].iloc[-1]:
        product_type_id= record_df['answer_id'].values[-2]
        table = record_df['answer_id_source'].values[-2]
        # query = f'''DELETE FROM {table} WHERE id={product_type_id}'''
        query = f'''UPDATE {table} SET deleted = 1 WHERE id = {product_type_id}''' 
        cursor.execute(query)
        con.commit()
        query = f'''UPDATE products_product SET deleted = 1 WHERE type_id = {product_type_id}''' 
        cursor.execute(query)
        con.commit()

    elif 68 in record_df['answer_id'].values.tolist() and success:# and 'success' in record_df['answer_type'].iloc[-1]:
        product_id= record_df['answer_id'].values[-2]
        table = record_df['answer_id_source'].values[-2]
        # query = f'''DELETE FROM {table} WHERE id={product_id}'''
        query = f'''UPDATE {table} SET deleted = 1 WHERE id = {product_id}''' 
        cursor.execute(query)
        con.commit()
            
    elif record_df['answer_id'].iloc[-1] in [62, 64]:
        mask = record_df['answer_id_source'] == 'users_user'
        id_list = record_df[mask]['answer_id'].values.tolist()   
        for id in id_list:
            # query = f'''DELETE FROM users_user WHERE id={id}'''
            query = f'''UPDATE users_user SET deleted = 1 WHERE id = {id}''' 
            cursor.execute(query)
            con.commit()
    elif record_df['answer_id'].iloc[-1] == 63:
        mask = record_df['answer_id_source'] == 'users_user'
        id_list = record_df[mask]['answer_id'].values.tolist()   
        for id in id_list:
            query = f'''UPDATE users_user SET confirmed = 1 WHERE id={id}'''
            cursor.execute(query)
            con.commit()

    elif record_df['answer_id'].iloc[-1] == 65:
        mask = record_df['answer_id_source'] == 'users_user'
        id_list = record_df[mask]['answer_id'].values.tolist()   
        for id in id_list:
            query = f'''UPDATE users_user SET user_type = "admin" WHERE id={id}'''
            cursor.execute(query)
            con.commit()

    elif record_df['answer_id'].iloc[-1] == 66:
        mask = record_df['answer_id_source'] == 'users_user'
        id_list = record_df[mask]['answer_id'].values.tolist()   
        for id in id_list:
            query = f'''UPDATE users_user SET user_type = "employee" WHERE id={id}'''
            cursor.execute(query)
            con.commit()
    
    # print(record_df)
        
    # users_df['date_submitted'] = datetime.now()
    # users_df['user_type'] = 'employee'
    # users_df.to_sql(con=con, name='users_user', if_exists='append', index=False)
    cursor.close()


