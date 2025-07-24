from flask import Flask,request,jsonify
import re
import pyotp
import base64
import mysql.connector
from flask_cors import CORS
from Data_Fetching import fetch_data_NS
from Model_1.model1_get_data import model1_get_data, model1_load_model, model1_predict
from Model_2.model2_get_data import model2_get_data, model2_load_model, model2_predict
from Model_3.model3_get_data import model3_get_data, model3_load_model, model3_predict
from Model_4.model4_get_data import model4_get_data, model4_load_model, model4_predict
from Email.email_page import send_mail
import time
import threading
from news_data.get_news import fetch_sentiment

# from news_data.sentimental_analysis import load_sentimental_model

conn = mysql.connector.connect(
    host="localhost",  # Change if using a remote database
    user="root", 
    password="password",
    database="stockgorithm"
)




app = Flask(__name__)
CORS(app)

model1, model1_scaler_x, model1_scaler_y = model1_load_model()
model2, model2_scaler_x, model2_scaler_y = model2_load_model()
model3, model3_scaler_x, model3_scaler_y = model3_load_model()
model4, model4_scaler_x, model4_scaler_y = model4_load_model()

def aironix_model1_prediction():
    test_data,current_close,datetime_stamp= model1_get_data(model1_scaler_x,model1_scaler_y)
    prediction_result = model1_predict(model1,test_data,model1_scaler_y)
    cursor = conn.cursor()

    sql_query = 'select predicted_close from airon where model_id = 1 order by id desc limit 1'
    cursor.execute(sql_query)
    prev_close = cursor.fetchone()
    print(prev_close)
    prev_close = prev_close[0]

    sql_query = 'insert into airon (model_id ,current_stock_name,current_close,predicted_close,time_stamp) values (%s,%s,%s,%s,%s)'
    values = (
        int(1),
        str('HDFCBANK'),
        float(current_close),
        float(prediction_result),
        str(datetime_stamp)
    )

    cursor.execute(sql_query,values)
    conn.commit()
    cursor.close()

    return


def aironix_model2_prediction():
    test_data,current_close,datetime_stamp= model2_get_data(model2_scaler_x,model2_scaler_y)
    prediction_result = model2_predict(model2,test_data,model2_scaler_y)
    cursor = conn.cursor()

    sql_query = 'select predicted_close from airon where model_id = 2 order by id desc limit 1'
    cursor.execute(sql_query)
    prev_close = cursor.fetchone()
    print(prev_close)
    prev_close = prev_close[0]

    sql_query = 'insert into airon (model_id ,current_stock_name,current_close,predicted_close,time_stamp) values (%s,%s,%s,%s,%s)'
    # values = (1,'HDFCBANK',float(current_close),float(prediction_result))
    values = (
        int(2),
        str('SBIN'),
        float(current_close),
        float(prediction_result),
        str(datetime_stamp)
    )

    cursor.execute(sql_query,values)
    conn.commit()
    cursor.close()
    return
   



def aironix_model4_prediction():
    test_data,current_close,datetime_stamp= model4_get_data(model4_scaler_x,model4_scaler_y)
    prediction_result = model4_predict(model4,test_data,model4_scaler_y)
    cursor = conn.cursor()

    sql_query = 'select predicted_close from airon where model_id = 4 order by id desc limit 1'
    cursor.execute(sql_query)
    prev_close = cursor.fetchone()
    print(prev_close)
    prev_close = prev_close[0]

    sql_query = 'insert into airon (model_id ,current_stock_name,current_close,predicted_close,time_stamp) values (%s,%s,%s,%s,%s)'
    values = (
        int(4),
        str('TATAMOTORS'),
        float(current_close),
        float(prediction_result),
        str(datetime_stamp)
    )

    cursor.execute(sql_query,values)
    conn.commit()
    cursor.close()
    return
 

def aironix_model3_prediction():
    test_data,current_close,datetime_stamp= model3_get_data(model3_scaler_x,model3_scaler_y)
    prediction_result = model3_predict(model3,test_data,model3_scaler_y)
    cursor = conn.cursor()

    sql_query = 'select predicted_close from airon where model_id = 3 order by id desc limit 1'
    cursor.execute(sql_query)
    prev_close = cursor.fetchone()
    print(prev_close)
    prev_close = prev_close[0]

    sql_query = 'insert into airon (model_id ,current_stock_name,current_close,predicted_close,time_stamp) values (%s,%s,%s,%s,%s)'
    # values = (1,'HDFCBANK',float(current_close),float(prediction_result))
    values = (
        int(3),
        str('INFY'),
        float(current_close),
        float(prediction_result),
        str(datetime_stamp)
    )

    cursor.execute(sql_query,values)
    conn.commit()
    cursor.close()
    return
    # return jsonify({
    #     'model_id':3,
    #     'predicted_close':float(prediction_result),
    #     'current_close':current_close,
    #     'status': 'NEGATIVE' if prev_close > prediction_result  else 'POSITIVE',
    #     'stock_name':"INFY"
    # })


def generate_otp():
    secret = base64.b32encode(b"MYSECRETKEY12345").decode('utf-8')    
    totp = pyotp.TOTP(secret, digits=6)
    return totp.now()

# Example Usage
print("Your OTP:", generate_otp())

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)is not None


@app.route('/signup',methods=['POST'])
def signup():
    parameters = request.get_json()

    if not parameters or 'email' not in parameters:
        return jsonify({"status": "error", "message": "Missing email field"}), 400
    
    if not is_valid_email(parameters['email']):
        return jsonify({"status":"error","email":parameters['email']}), 400
    
    otp = generate_otp()
    cursor = conn.cursor()
    sql_suery = "insert into signup_otp(email,otp)values (%s,%s)"
    values = (parameters['email'],otp)
    cursor.execute(sql_suery,values)
    conn.commit()
    cursor.close()
    status = send_mail(parameters,otp)
    if status == True:
        return jsonify({"status":"success","email":parameters['email']})
    else:
        return jsonify({"status":"error","email":parameters['email']})
    
@app.route("/signup_otp_verification",methods=['POST'])
def signup_otp_verification():
    data = request.get_json()

    if not data or 'otp' not in data:
        return jsonify({"status":"failed"}),400
    
    cursor  = conn.cursor()
    sql_query = "select count(*) from signup_otp where otp = %s"
    value = (data['otp'],)
    cursor.execute(sql_query,value)
    result = cursor.fetchone()[0]
    cursor.close()
    if result > 0:
        return jsonify({"status":"success","otp":data['otp']}),200
    else:
        return jsonify({"status":"failed"}),400

@app.route("/signup_user_details",methods=['POST'])
def signup_user_details():
    data = request.get_json()

    if not data:
        return jsonify({"status":"error"})
    
    cursor = conn.cursor()
    sql_query = "insert into user (username,password) values(%s,%s)"
    values = (data['username'],data['password'])
    cursor.execute(sql_query,values)
    conn.commit()
    cursor.close()
    return jsonify({'status':'success',"username":data['username'],"password":data['password']})


@app.route('/aironix/model_1_prediction', methods=['POST'])
def airon_model_1():
    conn = None
    cursor = None
    try:
        # 🔄 Create fresh connection for this request
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aswin@2004",
            database="stockgorithm"
        )
        cursor = conn.cursor()

        # 🔍 Query the last 2 prediction rows
        sql_query = '''
            SELECT predicted_close, current_close 
            FROM airon 
            WHERE model_id = 1  
            ORDER BY id DESC 
            LIMIT 2
        '''
        cursor.execute(sql_query)
        results = cursor.fetchall()

        if len(results) < 2:
            return jsonify({
                'status': 'NOT_ENOUGH_DATA',
                'message': 'Less than two predictions found for HDFCBANK'
            })

        last_prediction = results[0][0]
        second_last_prediction = results[1][0]

        status = 'POSITIVE' if last_prediction > second_last_prediction else 'NEGATIVE'

        return jsonify({
            'model_id': 1,
            'predicted_close': float(last_prediction),
            'current_close': results[0][1],
            'status': status,
            'stock_name': "HDFCBANK",
            'datetime': '2025-04-04 15:20:00'
        })

    except Exception as e:
        print("Error in /aironix/model_1_prediction:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/aironix/model_2_prediction',methods=['POST'])
def airon_model_2():
    cursor = conn.cursor()

    # Fetch the last 2 predicted_close values for HDFCBANK, model_id = 1
    sql_query = '''
        SELECT predicted_close,current_close 
        FROM airon 
        WHERE model_id = 2 
        ORDER BY id DESC 
        LIMIT 2
    '''
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) < 2:
        return jsonify({
            'status': 'NOT_ENOUGH_DATA',
            'message': 'Less than two predictions found for HDFCBANK'
        })

    last_prediction = results[0][0]
    second_last_prediction = results[1][0]

    status = 'POSITIVE' if last_prediction > second_last_prediction else 'NEGATIVE'

    return jsonify({
        'model_id':2,
        'predicted_close':float(last_prediction),
        'current_close':results[0][1],
        'status': status,
        'stock_name':"SBIN",
        'datetime':'2025-04-04 15:20:00'
    })


@app.route('/aironix/model_3_prediction',methods=['POST'])
def airon_model_3():
    cursor = conn.cursor()

    # Fetch the last 2 predicted_close values for HDFCBANK, model_id = 1
    sql_query = '''
        SELECT predicted_close,current_close 
        FROM airon 
        WHERE model_id = 3 
        ORDER BY id DESC 
        LIMIT 2
    '''
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) < 2:
        return jsonify({
            'status': 'NOT_ENOUGH_DATA',
            'message': 'Less than two predictions found for HDFCBANK'
        })

    last_prediction = results[0][0]
    second_last_prediction = results[1][0]

    status = 'POSITIVE' if last_prediction > second_last_prediction else 'NEGATIVE'

    return jsonify({
        'model_id':3,
        'predicted_close':float(last_prediction),
        'current_close':results[0][1],
        'status': status,
        'stock_name':"INFY",
        'datetime':'2025-04-04 15:20:00'
    })


@app.route('/aironix/model_4_prediction',methods=['POST'])
def airon_model_4():
    cursor = conn.cursor()

    # Fetch the last 2 predicted_close values for HDFCBANK, model_id = 1
    sql_query = '''
        SELECT predicted_close,current_close 
        FROM airon 
        WHERE model_id = 4 
        ORDER BY id DESC 
        LIMIT 2
    '''
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) < 2:
        return jsonify({
            'status': 'NOT_ENOUGH_DATA',
            'message': 'Less than two predictions found for HDFCBANK'
        })

    last_prediction = results[0][0]
    second_last_prediction = results[1][0]

    status = 'POSITIVE' if last_prediction > second_last_prediction else 'NEGATIVE'

    return jsonify({
        'model_id':4,
        'predicted_close':float(last_prediction),
        'current_close':results[0][1],
        'status': status,
        'stock_name':"TATAMOTORS",
        'datetime':'2025-04-04 15:20:00'
    })


@app.route('/fetch_data', methods=['POST'])
def fetch_data_NS_M():
    conn = None
    cursor = None
    try:
        # Get request parameters
        parameter = request.get_json()

        # Validate stock_name
        if not parameter or 'stock_name' not in parameter:
            return jsonify({"error": "Missing stock_name"}), 400

        # ✅ Create a new DB connection for this request
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aswin@2004",
            database="stockgorithm"
        )
        cursor = conn.cursor(dictionary=True)

        # ✅ Fetch stock data (likely from yfinance or custom source)
        data = fetch_data_NS.get_data(parameter['stock_name'])

        if not data:
            raise ValueError("No stock data returned")

        # ✅ Query about info from database
        sql_query = 'SELECT about FROM stock_details WHERE stock_name = %s'
        values = (parameter['stock_name'].strip(),)
        cursor.execute(sql_query, values)
        result = cursor.fetchone()

        if not result:
            raise ValueError("No description available for this stock")

        # ✅ Get last closing price from fetched data
        close_price = data[-1]['Close']

        # ✅ Return the structured JSON response
        return jsonify({
            'close_rate': close_price,
            'stock_name': parameter['stock_name'],
            'about': result['about'],
            'stock_data': data
        })

    except Exception as e:
        print("Parameter:", parameter)
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        # ✅ Clean up cursor and connection
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route('/signin',methods=['POST'])
def signin():
    parameters = request.get_json()
    cursor = conn.cursor()
    sql_query = 'SELECT COUNT(*) FROM user WHERE TRIM(username) = %s AND password = %s'
    values = (parameters['username'],parameters['password'])
    cursor.execute(sql_query,values)
    result = cursor.fetchone()
    print('result is :',result[0])
    cursor.close()
    return jsonify({
        'status':'approved' if result[0] >= 1 else 'invalid',
        'username':parameters['username'],
        'password':parameters['password']
        })


@app.route('/get_news',methods=['POST'])
def get_news():
    body = request.get_json()
    print(body)
    stock_news = fetch_sentiment()
    return jsonify({'news':stock_news})


@app.route('/aironix_premium_feature', methods=['POST'])
def best_stock_by_percentage_gain():
    cursor = conn.cursor()
    sql_query = '''WITH ranked AS (
                        SELECT *, ROW_NUMBER() OVER (PARTITION BY model_id ORDER BY time_stamp DESC) AS rn 
                        FROM airon
                   )
                   SELECT last.model_id, last.current_stock_name, 
                          second.predicted_close AS second_last_predicted_close, 
                          last.predicted_close AS last_predicted_close 
                   FROM ranked last 
                   JOIN ranked second ON last.model_id = second.model_id 
                   WHERE last.rn = 1 AND second.rn = 2 
                   ORDER BY last.model_id'''
    
    cursor.execute(sql_query)
    stock_data = cursor.fetchall()

    best = None
    max_gain = float('-inf')

    for model_id, current_stock_name, second_last_predicted_close, last_predicted_close in stock_data:
        if second_last_predicted_close == 0:
            continue  # Avoid division by zero

        percentage_gain = ((last_predicted_close - second_last_predicted_close) / second_last_predicted_close) * 100
        absolute_gain = last_predicted_close - second_last_predicted_close

        if percentage_gain > max_gain:
            max_gain = percentage_gain
            best = {
                "stock": current_stock_name,
                "percentage_gain": round(percentage_gain, 2),
                "absolute_gain": round(absolute_gain, 2),
                "last_price": round(last_predicted_close, 2)
            }
    cursor.close()
    return jsonify({'aironix_premium': best})

def call_every_5_minutes():
    while True:
        aironix_model1_prediction()
        aironix_model2_prediction()
        aironix_model3_prediction()
        aironix_model4_prediction()
        time.sleep(300)  # Sleep for 5 minutes

if __name__ == '__main__':
    # Start thread BEFORE running the app
    thread = threading.Thread(target=call_every_5_minutes)
    thread.daemon = True
    thread.start()
    app.run(debug=True)


