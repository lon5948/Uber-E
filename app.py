import os
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, session, request, jsonify, flash, redirect, url_for
from flask_paginate import Pagination
from werkzeug.utils import secure_filename
import mysql.connector
import datetime
import time

UPLOAD_FOLDER = 'static\\Picture'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = b'S\xc5\xf5\xf4!\x9d=S\t\xb4\xb8\xcb\xb5\x16\x1cfXj\xde\x85\xe7\xf5\xe4\xe2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SESSION_TYPE = 'redis'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db"
)
cursor = db.cursor(buffered=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    uid = session.get('uid', None)
    if uid is not None:
        session.pop('uid')
    return render_template('index.html')

# index


@app.route('/validateUser', methods=['POST'])
def validateUser():
    Account = request.form.get('Account')
    cursor.execute("select * from user where binary account = %s", (Account, ))
    res = cursor.fetchall()
    result = dict()
    if len(res) > 0: 
        result['nameResult'] = 'This account is used'
        result['error'] = True
    elif Account=='':
        result['nameResult'] = 'Account name is required'
        result['error'] = True
    else:
        result['nameResult'] = ''
        result['error'] = False
    return jsonify(result)


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='POST':
        name = request.form.get('name')
        password = request.form.get('password')
        phonenumber = request.form.get('phonenumber')
        Account = request.form.get('Account')
        re_password = request.form.get('re-password')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        error = None
        if name=='':
            error = 'Username is required.'
        elif phonenumber=='':
            error = 'phonenumber is required.'
        elif Account=='':
            error = 'account is required.'
        elif password=='':
            error = 'Password is required.'
        elif re_password=='':
            error = 're-type Password is required.'
        elif latitude=='':
            error = 'latitude is required.'
        elif longitude=='':
            error = 'longitude is required.'
        elif password!=re_password:
            error = 're-type password does not match'
        elif password.isalnum()==False or Account.isalnum()==False:
            error = 'Account and password format error'
        elif name.isalpha()==False:
            error = 'name format error'
        elif phonenumber.isdigit()==False or len(phonenumber)!=10:
            error = 'phonenumber format error'
        else:
            try:
                float(latitude)
                float(longitude)
                if float(latitude)>90 or float(latitude)<-90:
                    error = 'invalid latitude format'
                if float(longitude)>180 or float(longitude)<-180:
                    error = 'invalid longitude format'
            except ValueError:
                error = 'wrong latitude/longtitude format'
            
        cursor.execute("select MAX(uid) from user")
        maxuid = cursor.fetchone()[0]
        if maxuid is None:
            maxuid = 0
        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO user (uid,name, password,account,phone,latitude,longitude,wallet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(str(maxuid+1),name, bcrypt.generate_password_hash(password),Account,phonenumber,latitude,longitude,0),)
                db.commit()
            except mysql.connector.IntegrityError:
                error = f"Account {Account} is already registered"
            else:
                flash('Register success!',category='success')
                return redirect(url_for('login'))
        flash(error,category='danger')
    return render_template('sign-up.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=='POST':
        Account = request.form.get('Account')
        password = request.form.get('password')
        error = None
        cursor.execute('SELECT * FROM user WHERE binary account = %s', (Account,))
        accountdata = cursor.fetchone()
        if accountdata is None:
            error = 'Account not registered!'
        elif bcrypt.check_password_hash(accountdata[2], password)==False:
            error = 'Incorrect password!'
        if error is None:
            session.clear()
            session['uid'] = accountdata[0]
            return redirect(url_for('main'))
        flash(error,category='danger')
    try:
        uid = session['uid']
        if uid is not None:
            session.pop('uid')
    except KeyError:
        _ = False
    return render_template('index.html')


# main
@app.route('/main', methods=['GET'])
def main():
    def getShopOrder(s):
        ss = session.get('shopOrderStatus', 'All')
        if ss == "All":
            cursor.execute("""
            select orders.oid, status, start, end, user.name, type, subtotal, delivery_fee, total
            from orders natural join user
            where sid = %s
            """, (s, ))
        else:
            cursor.execute("""
            select orders.oid, status, start, end, user.name, type, subtotal, delivery_fee, total
            from orders natural join user
            where sid = %s and status = %s
            """, (s, ss, ))
        t_order = cursor.fetchall()
        re = list()
        for o in t_order:
            cursor.execute("""
            select image, name, price, quantity from iteminorder
            where oid = %s
            """, (o[0], ))
            r = dict()
            r["oid"] = o[0]
            r["status"] = o[1]
            r["start"] = o[2]
            r["end"] = o[3] if o[3] is not None else ''
            r["userName"] = o[4]
            r["type"] = o[5]
            r["subtotal"] = o[6]
            r["d_fee"] = o[7]
            r["total"] = o[8]

            r["orderItem"] = cursor.fetchall()
            re.append(r)
        return re
    def getMyOrder(uid):
        status=session.get('myOrderStatus','All')
        if status == 'All':
            cursor.execute("select oid,status,start,end,sid,total,subtotal,delivery_fee from orders where uid=%s",(uid,))
        elif status == 'Finished':
            cursor.execute("select oid,status,start,end,sid,total,subtotal,delivery_fee from orders where uid=%s and status=%s",(uid,'Finished',))
        elif status == 'Not finish':
            cursor.execute("select oid,status,start,end,sid,total,subtotal,delivery_fee from orders where uid=%s and status=%s",(uid,'Not finish',))
        elif status == 'Cancel':
            cursor.execute("select oid,status,start,end,sid,total,subtotal,delivery_fee from orders where uid=%s and status=%s",(uid,'Cancel',))   
        tempList = cursor.fetchall()
        print(tempList)
        orderList = []
        for temp in tempList:
            sid = temp[4]
            cursor.execute("select shopname from shop where sid=%s",(sid,))
            shopname = cursor.fetchone()[0]
            cursor.execute("select image, name, price, quantity from iteminorder where oid = %s", (temp[0], ))
            orderDetail = cursor.fetchall()
            print(orderDetail)
            tup = (temp[0],temp[1],temp[2],temp[3],shopname,temp[5],orderDetail,temp[6],temp[7])
            orderList.append(tup)
        return orderList
    uid = session.get('uid')
    if uid is None:
        return redirect('login')
    sid = None
    sss = session.get('shopOrderStatus', 'All')
    mystatus = session.get('myOrderStatus', 'All')
    defaultPage = session.get('defaultPage', 'home')
    userShop = None
    userShopItems = list()
    if session.get('shopList') is not None:
        shopList = session.get('shopList')
    else:
        shopList = list()
    if session.get('itemList') is not None:
        itemList = session.get('itemList')
        session.pop('itemList')
    else:
        itemList = list()
    if session.get('recordList') is not None:
        recordList = session.get('recordList')
    else:
        recordList = list()
    if session.get('orderList') is not None:
        orderList = session.get('orderList')
    else:
        orderList = list()
    
    def get_shop(offset, per_page):
        return shopList[offset: offset + per_page]

    userInfo = dict()
    if uid is not None:
        cursor.execute("select account,name,phone,longitude,latitude,wallet from user where uid = %s", (uid, ))
        info = cursor.fetchone()
        cursor.execute("select uid from shop where uid = %s", (uid, ))
        if cursor.fetchone() is None: 
            role = "USER" 
        else: 
            role = "MANAGER"
        userInfo = {
            'account': info[0],
            'role': role,
            'name': info[1],
            'phone': info[2],
            'longitude': info[3],
            'latitude': info[4],
            'wallet': info[5]
        }
        session['name'] = info[1]
        session['money'] = info[5]
        cursor.execute("select shopname, shoptype, latitude, longitude, sid from shop where uid = %s", (uid, ))
        res = cursor.fetchall()
        if len(res) > 0:
            tmp = res[0]
            userShop = {
                'shopName': tmp[0],
                'shopType': tmp[1],
                'latitude': tmp[2],
                'longitude': tmp[3]
            }
            sid = tmp[4]
            cursor.execute("select name, price, quantity, image, iid from item where sid = %s", (sid, ))
            userShopItems = cursor.fetchall()
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    total = len(shopList)
    pagination_shop = get_shop(offset, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    print(mystatus)
    print(orderList)
    return render_template(
        'nav.html', page=page, per_page=per_page, pagination=pagination, userInfo=userInfo,
        recordList=recordList, userShop=userShop, shops=pagination_shop, userShopItems=userShopItems, itemList=itemList,
        shopOrderList=getShopOrder(sid), shopOrderStatus=sss, defaultPage=defaultPage, orderList=getMyOrder(uid),myOrderStatus=mystatus
    )

# home
@app.route('/editLocation', methods=['POST'])
def editLocation():
    uid = session.get('uid')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    try:
        if float(longitude)>180 or float(longitude)<-180 or float(latitude)>90 or float(latitude)<-90:
            flash(" Format Error ! ", category='danger')
        else:
            cursor.execute(" update user set longitude = %s, latitude = %s where uid = %s ", (longitude, latitude, uid, ))
            db.commit()
            flash(" Successfully Update ! ", category='success')
    except:
        flash(" Format Error ! ", category='danger')
    session['defaultPage'] = 'home'
    return redirect(url_for('main'))

@app.route('/addMoney', methods=['POST'])
def addMoney():
    uid = session.get('uid')
    cursor.execute("select name,wallet from user where uid = %s ", (uid, ))
    info = cursor.fetchone()
    wallet = info[1]
    value = request.form.get('value')
    try:
        if int(value)<=0:
            flash("Value Format Error!", category='danger')
        else:
            wallet += int(value)
            Time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute(" update user set wallet = %s where uid = %s ", (wallet, uid, ))
            db.commit()
            cursor.execute("insert into record (uid, action, time, trader, amountChange) values (%s, %s, %s, %s, %s)",(uid, 'Recharge', Time, info[0], '+'+value,))
            db.commit()
            flash(" Successfully Add Money! ", category='success')
    except:
        flash("Value Format Error!", category='danger')
    session['defaultPage'] = 'home'
    return redirect(url_for('main'))

@app.route('/search', methods=['POST'])
def search():
    uid = session.get('uid')
    cursor.execute("""select longitude,latitude from user where uid=%s """, (uid,))
    userLocation = cursor.fetchone()
    longitude = userLocation[0]
    latitude = userLocation[1]
    shopList = list()
    checkList = list()
    # keyword of shop.name
    keyword = request.form.get('keyword')
    if keyword != "":
        cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where shopname like %s """, (longitude,latitude,'%'+keyword+'%',))
        shopList = cursor.fetchall()
    # distance of user and shop
    distance = request.form.get('distance')
    if distance == 'near':
        cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)) as distance,sid from shop where ST_Distance_Sphere(point(%s,%s),point(longitude,latitude))<=5000 """, (longitude,latitude,longitude,latitude,))
    elif distance == 'medium':
        cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where ST_Distance_Sphere(point(%s,%s),point(longitude,latitude))>5000 and ST_Distance_Sphere(point(%s,%s),point(longitude,latitude))<=15000 """, (longitude,latitude,longitude,latitude,longitude,latitude,))
    elif distance == 'far':
        cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where ST_Distance_Sphere(point(%s,%s),point(longitude,latitude))>15000 """, (longitude,latitude,longitude,latitude,))
    if distance != '--- select ---':
        if len(shopList) == 0:
            shopList = cursor.fetchall()
        else :
            checkList = cursor.fetchall()
            if len(checkList) != 0:
                newList = [shop for shop in shopList if shop in checkList]
                shopList = newList
    # the range of price
    minPrice = request.form.get('minPrice')
    maxPrice = request.form.get('maxPrice')
    if minPrice == '' and maxPrice != '':
        minPrice = 0
    elif maxPrice == '' and minPrice != '':
        maxPrice = 1e9
    if minPrice!='' and maxPrice!='':
        cursor.execute("""select distinct sid from item where price>=%s and price<=%s """, (minPrice,maxPrice,))
        sids = cursor.fetchall()
        for sid in sids:
            sid = sid[0]
            cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where sid=%s""", (longitude,latitude,sid,))
            checkList.append(cursor.fetchone())
        if len(shopList) == 0:
            shopList = checkList
        elif len(checkList) != 0:
            newList = [shop for shop in shopList if shop in checkList]
            shopList = newList
    # keyword of meal 
    meal = request.form.get('meal')
    if meal != "":
        cursor.execute("""select distinct sid from item where name like %s """, ('%'+meal+'%',))
        sids = cursor.fetchall()
        for sid in sids:
            sid = sid[0]
            cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where sid=%s""", (longitude,latitude,sid,))
            checkList.append(cursor.fetchone())
        if len(shopList) == 0:
            shopList = checkList
        elif len(checkList) != 0:
            newList = [shop for shop in shopList if shop in checkList]
            shopList = newList
    # shoptype
    category = request.form.get('category')
    if category != "":
        cursor.execute("""select shopname,shoptype,ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where shoptype like %s """, (longitude,latitude,'%'+category+'%',))
        if len(shopList) == 0:
            shopList = cursor.fetchall()
        else:
            checkList = cursor.fetchall()
            if len(checkList) != 0:
                newList = [shop for shop in shopList if shop in checkList]
                shopList = newList
    # change distance into ['near','medium','far'] 
    for index,shop in enumerate(shopList):
        shop = list(shop)
        if float(shop[2]) < 5000:
            shop[2] = 'near'
        elif float(shop[2]) > 15000:
            shop[2] = 'far'
        else:
            shop[2] = 'medium'
        shop = tuple(shop)
        shopList[index] = shop
    session['shopList'] = shopList
    session['defaultPage'] = 'home'
    return redirect(url_for('main'))

@app.route('/openMenu',methods=['POST'])
def openMenu():
    sid = request.form.get('sid')
    session['sid'] = sid
    cursor.execute("""select image,name,price,quantity from item where sid=%s """, (sid,))
    itemList = cursor.fetchall()
    retList = list()
    for index,item in enumerate(itemList):
        itemDict = dict()
        itemDict['index'] = index+1
        itemDict['picture'] = item[0]
        itemDict['name'] = item[1]
        itemDict['price'] = item[2]
        itemDict['quantity'] = item[3]
        retList.append(itemDict)
    return jsonify(retList)

@app.route('/validateQuantity', methods=['POST'])
def validateQuantity():
    result = dict()
    length = request.form.get('length')
    for i in range(int(length)):
        num = request.form.get(str(i+1))
        try:
            if num != '':
                if int(num) <= 0: 
                    result['nameResult'] = 'Order Quantity Format Error'
                    result['error'] = True
                    return jsonify(result)
        except:
            result['nameResult'] = 'Order Quantity Format Error'
            result['error'] = True
            return jsonify(result)
    return jsonify(result)

@app.route('/calculatePrice',methods=['POST'])
def calculatePrice():
    uid = session['uid']
    sid = session['sid']
    type = request.form.get('type')
    session['type'] = type
    if type == 'Delivery':
        cursor.execute("""select longitude,latitude from user where uid=%s """, (uid,))
        userLocation = cursor.fetchone()
        longitude = userLocation[0]
        latitude = userLocation[1]
        cursor.execute("""select ST_Distance_Sphere(point(%s,%s),point(longitude,latitude)),sid from shop where sid=%s """, (longitude,latitude,sid,))
        distance = cursor.fetchone()[0]
        session['distance'] = distance
        if distance < 1000:
            deliveryFee = 10
        else:
            deliveryFee = round((distance/1000)*10)
    else:
        deliveryFee = 0
    cursor.execute("""select image,name,price,quantity from item where sid=%s """, (sid,))
    itemList = cursor.fetchall()
    subtotal = 0
    orderDict = dict()
    length = 0
    for i,item in enumerate(itemList):
        num = request.form.get(str(i+1))
        if num != '':
            subtotal += int(num)*int(item[2])
            orderList = list()
            length += 1
            orderList.append(length)
            orderList.append(item[0]) 
            orderList.append(item[1]) 
            orderList.append(item[2]) 
            orderList.append(num)
            orderDict[str(length)] = orderList
    orderDict['subtotal'] = subtotal
    orderDict['delivery'] = deliveryFee
    orderDict['total'] = subtotal + deliveryFee
    orderDict['length'] = length
    session['deliveryFee'] = deliveryFee
    session['subtotal'] = subtotal
    session['total'] = subtotal + deliveryFee
    return jsonify(orderDict)

@app.route('/order',methods=['POST'])
def order():
    uid = session['uid']
    sid = session['sid']
    type = session['type']
    distance = session['distance']
    subtotal = session['subtotal']
    deliveryFee = session['deliveryFee']
    cursor.execute("""select shopname,uid from shop where sid=%s """, (sid,))
    info = cursor.fetchone()
    shopName = info[0]
    uidShop = info[1]
    cursor.execute("""select wallet from user where uid=%s """, (uidShop,))
    walletShop = cursor.fetchone()[0]
    cursor.execute("""select quantity,name,iid,price,image from item where sid=%s """, (sid,))
    itemList = cursor.fetchall()
    money = session['money']
    name = session['name']
    total = session['total']
    error = ''
    errorList = list()
    dic = dict()
    for i,item in enumerate(itemList):
        num = request.form.get('a'+str(i+1))
        if num != '':
            dic[item[2]] = [num,item[3],item[4]]
        else:
            num = 0
        if int(num) > int(item[0]):
            errorList.append(item[1])
    if len(errorList) != 0:
        error = "Order Quantity > Shop Quantity  --> "
        for e in errorList:
            error +=  e + ' | '
        error = error[0:len(error)-2]
        flash(error,category='danger')
    elif money < total:
        flash("Insufficient Balance",category='danger')
    else:
        Time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute("insert into orders (status,start,distance,total,type,uid,sid,delivery_fee,subtotal) values ('Not finish',%s,%s,%s,%s,%s,%s,%s,%s)",(Time,distance,total,type,uid,sid,deliveryFee,subtotal))
        db.commit()
        cursor.execute("select oid from orders where start=%s and total=%s and type=%s and uid=%s and sid=%s and delivery_fee=%s and subtotal=%s",(Time,total,type,uid,sid,deliveryFee,subtotal))
        print((Time,distance,total,type,uid,sid,deliveryFee,subtotal))
        oid = cursor.fetchone()[0]
        for key,value in dic.items():
            cursor.execute("select quantity from item where iid = %s", (key,))
            q = cursor.fetchone()[0]
            q -= int(value[0])
            cursor.execute("update item set quantity = %s where iid = %s", (q,key, ))
            db.commit()
            cursor.execute("insert into iteminorder (oid,iid,quantity,name,price,image) values (%s,%s,%s,%s,%s,%s)",(oid,key,value[0],name,value[1],value[2],))
            db.commit()
        money -= total
        walletShop += total
        cursor.execute("update user set wallet = %s where uid = %s", (money,uid ))
        db.commit()
        cursor.execute("""insert into record (uid, action, time, trader, amountChange) values (%s, %s, %s, %s, %s)""",(uid, 'Payment', Time, shopName, str(-total)))
        db.commit()
        cursor.execute("update user set wallet = %s where uid = %s", (walletShop,uidShop))
        db.commit()
        cursor.execute("""insert into record (uid, action, time, trader, amountChange) values (%s, %s, %s, %s, %s)""",(uidShop, 'Receive', Time, name, '+'+str(total)))
        db.commit()
        flash("Successfully Order",category='success')
    session['defaultPage'] = 'home'
    return redirect(url_for('main'))

# shop
@app.route('/validateShopInfo', methods=['POST'])
def validateShopInfo():
    def check_num(x, s):
        try:
            a = float(x)
            if s == 'longitude':
                if a > 180.0 or a < -180.0:
                    return False
            else:
                if a > 90.0 or a < -90.0:
                    return False
            return True
        except ValueError:
            return False

    shopName = request.form.get('name')
    shopType = request.form.get('type')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    if shopName + shopType + longitude + latitude == '':
        return jsonify({'error': True})
    cursor.execute("select * from shop where shopname = %s", (shopName, ))
    res = cursor.fetchall()
    result = dict()
    result['nameResult'] = 'This Name is used!' if len(res) > 0 else \
        'Shop Name should be at least one character!' if shopName == '' else ''
    result['typeResult'] = 'Shop Name should longer than 0' if shopType == '' else ''
    result['longitudeResult'] = 'Longitude format Error' if check_num(longitude, 'longitude') is False else ''
    result['latitudeResult'] = 'Latitude format Error' if check_num(latitude, 'latitude') is False else ''
    result['error'] = False if result['nameResult'] + result['typeResult'] + result['longitudeResult'] + \
        result['latitudeResult'] == '' else True
    return jsonify(result)

@app.route('/registerShop', methods=['POST'])
def registerShop():
    uid = session.get('uid')
    cursor.execute("select shopname from shop where uid = %s", (uid,))
    r = cursor.fetchall()
    if len(r) == 0:
        shopName = request.form.get('shopName')
        shopType = request.form.get('shopType')
        longitude = request.form.get('shopLongitude')
        latitude = request.form.get('shopLatitude')
        cursor.execute("""insert into shop (uid, shopname, shoptype, latitude, longitude, location)
                            values (%s, %s, %s, %s, %s, ST_GeomFromText(%s));"""
                       , (uid, shopName, shopType, latitude, longitude, f'POINT({latitude} {longitude})',))
        db.commit()
    flash("Successfully Registered.", category='success')
    session['defaultPage'] = 'menu1'
    return redirect(url_for('main'))


@app.route('/validateItemInfo', methods=['POST'])
def validateItemInfo():
    def check_num(x):
        try:
            a = int(x)
            if a > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    itemName = request.form.get('name')
    itemPrice = request.form.get('price')
    itemQuantity = request.form.get('quantity')
    picLength = request.form.get('pic')

    if itemName + itemPrice + itemQuantity == '' and picLength == '0':
        return jsonify({'error': True})

    result = dict()
    result['nameResult'] = 'Food Name should be at least one character!' if itemName == '' else ''
    result['priceResult'] = 'Price format Error' if check_num(itemPrice) is False else ''
    result['quantityResult'] = 'Quantity format Error' if check_num(itemQuantity) is False else ''
    result['picResult'] = 'Please select a file' if picLength == '0' else ''
    result['error'] = False if result['nameResult'] + result['priceResult'] + result['quantityResult'] + \
        result['picResult'] == '' else True
    return jsonify(result)


@app.route('/registerItem', methods=['POST'])
def registerItem():
    uid = session.get('uid')
    cursor.execute("select sid from shop where uid = %s", (uid,))
    sid = cursor.fetchall()[0][0]
    itemName = request.form.get('itemName')
    itemPrice = request.form.get('itemPrice')
    itemQuantity = request.form.get('itemQuantity')
    pic = request.files['itemPic']
    if allowed_file(pic.filename) is False:
        flash('Incapable file', category='danger')
        return redirect(url_for('main'))
    cursor.execute("SELECT name FROM item WHERE name = %s", (itemName, ))
    if len(cursor.fetchall()) > 0:
        flash('Duplicated item name!', category='danger')
        return redirect(url_for('main'))
    picName = secure_filename(pic.filename)
    fileName = str(time.time_ns()) + '.' + picName.rsplit('.', 1)[-1].lower()
    pic.save(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], fileName))
    cursor.execute("""insert into item (sid, name, quantity, price, image) VALUES (%s, %s, %s, %s, %s)""",
                   (sid, itemName, itemQuantity, itemPrice, fileName))
    db.commit()
    flash("Add success!", category='success')
    session['defaultPage'] = 'menu1'
    return redirect(url_for('main'))

@app.route('/updateItem', methods=['POST'])
def updateItem():
    def check_num(x):
        try:
            a = int(x)
            if a <= 0:
                return False
            return True
        except ValueError:
            return False
    itemId = request.form.get('itemId')
    itemQuantity = request.form.get('Quantity')
    itemPrice = request.form.get('Price')
    if check_num(itemQuantity) and check_num(itemPrice):
        cursor.execute("UPDATE item SET quantity = %s, price = %s WHERE iid = %s", (itemQuantity, itemPrice, itemId, ))
        db.commit()
        flash('Update Success!', category='success')
    elif itemQuantity == '' or itemPrice == '':
        flash('Update Error! Input is Empty.', category='danger')
    else:
        flash('Update Error! Input format Error.', category='danger')
    session['defaultPage'] = 'menu1'
    return redirect(url_for('main'))


@app.route('/deleteItem', methods=['POST'])
def deleteItem():
    itemId = request.form.get('itemId')
    cursor.execute("DELETE FROM item where iid = %s", (itemId, ))
    db.commit()
    flash('Delete Success.', category='success')
    session['defaultPage'] = 'menu1'
    return redirect(url_for('main'))

# transaction record
@app.route('/transactionRecord', methods=['POST'])
def transactionRecord():
    uid = session.get('uid')
    action = request.form.get('transactionAction')
    if action == 'All':
        cursor.execute("""select * from record where uid=%s """,(uid,))
    else:
        cursor.execute("""select * from record where action=%s and uid=%s """, (action,uid,))
    recordList = cursor.fetchall()
    session['recordList'] = recordList
    session['defaultPage'] = 'transaction'
    return redirect(url_for('main'))

#shopOrder
@app.route('/shopOrder', methods=['POST'])
def shopOrder():
    status = request.form.get('shopOrderStatus')
    session['shopOrderStatus'] = status
    session['defaultPage'] = 'shopOrder'
    return redirect(url_for('main'))

@app.route('/shopOrderDone', methods=['POST'])
def shopOrderDone():
    selected = request.form.getlist("shopOrderSelected")
    session['defaultPage'] = 'shopOrder'
    if len(selected) == 0:
        flash('Nothing selected!', category='danger')
        return redirect(url_for('main'))
    cursor.executemany(
        """UPDATE orders SET status = 'Finished', end = %s where oid = %s""",
        [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), _) for _ in selected]
    )
    db.commit()
    flash('Updated to Done!', category='success')
    return redirect(url_for('main'))

@app.route('/shopOrderCancel', methods=['POST'])
def shopOrderCancel():
    session['defaultPage'] = 'shopOrder'
    selected = request.form.getlist("shopOrderSelected")
    if len(selected) == 0:
        flash('Nothing selected!', category='danger')
        return redirect(url_for('main'))
    OwnerUid = session.get('uid')
    cursor.execute(
        """SELECT total, uid, name from orders natural join user where oid IN ({})""".format(','.join(selected))
    )
    refunds = cursor.fetchall()
    totalRefund = sum([a[0] for a in refunds])
    cursor.execute("""SELECT wallet from user where uid = %s""", (OwnerUid, ))
    remain = cursor.fetchall()[0][0]
    if remain < totalRefund:
        flash('Insufficient balance', category='danger')
        return redirect(url_for('main'))
    cursor.execute("SELECT shopname from shop where uid = %s", (OwnerUid, ))
    sn = cursor.fetchall()[0][0]
    cursor.executemany(
        """UPDATE orders SET status = 'Cancel', end = %s where oid = %s""",
        [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), _) for _ in selected]
    )
    cursor.execute("""UPDATE user SET wallet = wallet - %s WHERE uid = %s""", (totalRefund, OwnerUid, ))
    cursor.execute(
        """
        INSERT INTO record (action, time, trader, amountChange, uid) VALUES ("Payment", %s, %s, %s, %s);
    """, [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), a[2], '-{}'.format(a[0]), a[1]) for a in refunds]
    )
    cursor.executemany(
        """
        UPDATE user SET wallet = wallet + %s WHERE uid = %s
        """, refunds
    )
    cursor.executemany(
        """
        INSERT INTO record (action, time, trader, amountChange, uid) VALUES ("Receive", %s, %s, %s, %s);
        """, [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), sn, '{:+d}'.format(a[0]), a[1]) for a in refunds]
    )
    db.commit()
    flash('Order Cancelled!', category='success')
    return redirect(url_for('main'))

#myorder record
@app.route('/myorderRecord',methods=['POST'])
def myorderRecord():
    status = request.form.get('myOrderStatus')
    session['myOrderStatus'] = status
    session['defaultPage'] = 'myOrder'
    return redirect(url_for('main'))

@app.route('/cancelOrder',methods=['POST'])
def cancelOrder():
    session['defaultPage'] = 'myOrder'
    selected = request.form.getlist("myOrderSelected")
    if len(selected) == 0:
        flash('Nothing selected!', category='danger')
        return redirect(url_for('main'))
    uid = session.get('uid')
    cursor.execute("select name from user where uid=%s",(uid,))
    name = cursor.fetchone()[0]
    cursor.executemany(
        """UPDATE orders SET status = 'Cancel', end = %s where oid = %s""",
        [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), _) for _ in selected]
    )
    cursor.execute(
        """SELECT total, shop.uid,shop.shopname from orders natural join shop where oid IN ({})""".format(','.join(selected))
    )
    refunds = cursor.fetchall()
    walletUID = [[a[0],a[1]] for a in refunds]
    #update shop
    cursor.executemany(
        """
        UPDATE user SET wallet = wallet - %s WHERE uid = %s
        """, walletUID
    )
    cursor.executemany(
        """
        INSERT INTO record (action, time, trader, amountChange, uid) VALUES ("Payment", %s, %s, %s, %s);
        """, [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),name,'{:+d}'.format(a[0]), a[1]) for a in refunds]
    )
    #update user
    totalEarn=0
    for refund in refunds:
        totalEarn+=refund[0]
    cursor.execute("update user set wallet = wallet-%s where uid = %s",(totalEarn,uid,))
    cursor.executemany("""insert into record (action, time, trader, amountChange, uid) values ("Receive",%s,%s,%s,%s);""",
    [(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),a[2],'{:+d}'.format(a[0]), uid) for a in refunds])
    
    db.commit()
    flash('Successfully Cancel!', category='success')
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)