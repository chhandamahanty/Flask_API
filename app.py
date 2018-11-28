from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import requests


app = Flask(__name__)


@app.route('/search', methods=["POST"])
def search():
    user_input = request.get_json()
    #user_input = request.form["item"]
    temp_df = df_item_list[df_item_list['item'] == user_input['item']]
    if temp_df.shape[0] == 1:
        return jsonify({"status": "found", "item": temp_df['item'].values[0], "price" : str(temp_df['price'].values[0])})
    else:
        return jsonify({"status": "not_found"})


@app.route('/cart', methods=["POST"])
def cart():
    global df_shopping_cart
    user_input = request.get_json()
    shopping_item = user_input['shopping_item']
    shopping_quantity = user_input['shopping_quantity']
    try:
        df_shopping_cart = df_shopping_cart.append(pd.DataFrame([[shopping_item,shopping_quantity]], columns=['shopping_item', 'quantity']))
        df_shopping_cart.to_csv(r'./shopping_cart.csv', index=False)
        return jsonify({"status": "successful"})
    except:
        return jsonify({"status": "unsuccessful"})


@app.route('/show_cart', methods=["POST"])
def show_cart():
    global df_shopping_cart
    if df_shopping_cart.shape[0] == 0:
        return jsonify({"status": "empty_cart"})
    else:
        temp_df = df_shopping_cart.merge(df_item_list, how='left', left_on='shopping_item', right_on='item')
        temp_df['total'] = temp_df['quantity'].astype(int) * temp_df['price'].astype(int)
        shopping_item = list(temp_df['shopping_item'])
        quantity = list(temp_df['quantity'])
        price = list(temp_df['price'])
        total = list(temp_df['total'])
        cart_total = np.sum(temp_df['total'])
        #return jsonify({"status": "found_cart", "shopping_item": shopping_item, "quantity": quantity, "price": price, "total": total, "cart_total": str(cart_total)})
        return jsonify({"status": "found_cart", "cart_total": str(cart_total)})



@app.route('/del_cart', methods=["POST"])
def del_cart():
    global df_shopping_cart
    df_shopping_cart = pd.DataFrame(columns=['shopping_item', 'quantity'])
    return jsonify({"status": "successful"})

if __name__ == '__main__':

    df_item_list = pd.read_csv('./item_list.csv')
    df_shopping_cart = pd.DataFrame(columns=['shopping_item', 'quantity'])
    print('Read data successful')
    app.run(host="0.0.0.0", port=3333)