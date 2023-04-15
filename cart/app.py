from flask import *
from flask_session import Session
import stripe
app=Flask(__name__)
app.secret_key='@cartpy'
app.config['SESSION_TYPE']='filesystem'
stripe.api_key='sk_test_51MvxA3SFfQ9GS1uMun93VjtgduzbE42ktqAFkT7UUTBADB1sXZ0WFXnlURZ8ArmauQn6FVu28VBZ9GBTyrigIWr70032sLpFzP'
Session(app)
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dessert'))
    username='admin'
    password_a='admin'
    if request.method=='POST':
        user=request.form['user']
        password=request.form['password']
        if username==user and password==password_a:
            session['user']=user
            session['cart']={}
            return redirect(url_for('dessert'))
        flash('invalid credentials')
    return render_template('loginpage.html')
@app.route('/desserts')
def dessert():
    return render_template('dessertsPage.html')
@app.route('/cart/<name>/<price>/<path:imgurl>')
def cart(name,price,imgurl):
    if name not in session['cart']:
        session['cart'][name]=[price,imgurl]
        session.modified=True
        print(session['cart'])
        flash(f'{name} added to cart')
        return redirect(url_for('dessert'))
    
    flash('Item already in cart')
    return redirect(url_for('dessert'))
@app.route('/viewcart')
def viewcart():
    data=session['cart']
    return render_template('cart.html',data=data)
@app.route('/remcart/<item>')
def rem(item):
    if session.get('user'):
        session['cart'].pop(item)
        return redirect(url_for('viewcart'))
    return redirect(url_for('login'))
@app.route('/pay/<name>/<price>',methods=['POST'])
def pay(name,price):
    q=request.form['quantity']
    checkout_session=stripe.checkout.Session.create(
        success_url=url_for('dessert',_external=True),
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': name,
                    },
                    'unit_amount': int(price)*100,
                    'currency': 'inr',
                },
                'quantity': int(q),
            },
            ],
        mode="payment",)
    return redirect(checkout_session.url)


app.run(debug=True,use_reloader=True)




