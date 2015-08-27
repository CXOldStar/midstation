#-*-coding:utf-8
__author__ = 'qitian'

from midstation.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    wechat_id = db.Column(db.String(200), unique=True)
    telephone = db.Column(db.String(15), unique=True)
    mobile_phone = db.Column(db.String(15), unique=True)

    # One-to-many
    buttons = db.relationship("Button", backref="user",
                              primaryjoin="Button.user_id == User.id",
                              cascade='all, delete-orphan'
                              )
    #One-to-many
    services = db.relationship('Service',
                               backref='user',
                               primaryjoin='Service.user_id == User.id',
                               cascade='all, delete-orphan'
                               )
    # One-to-many
    customers = db.relationship('Customer',
                                backref='user',
                                primaryjoin='Customer.user_id == User.id',
                                cascade='all, delete-orphan'
                                )

    # One-to-many
    orders = db.relationship('Order',
                             backref='user',
                             primaryjoin='Order.user_id == User.id',
                             cascade='all, delete-orphan'
                             )

    def __init__(self, username, wechat_id=None, telephone=None, mobile_phone=None):
        self.username = username
        self.wechat_id = wechat_id
        self.telephone = telephone
        self.mobile_phone = mobile_phone

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """
        Saves a user and return a user object.
        :param username: user name
        :param wechat_id: wechat id
        :param telephone:
        :param mobile_phone:
        :return:
        """
        if self.id:
            db.session.add(self)
        else:
            db.session.add(self)

        db.session.commit()
        return self

    def delete(self):
        """
        delete a user
        :return:
        """
        db.session.delete(self)
        db.session.commit()


class Button(db.Model):
    __tablename__ = 'buttons'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    orders = db.relationship('Order',
                             primaryjoin="Order.button_id == Button.id"
                             )

    def __init__(self, node_id):
        self.node_id = node_id

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None, service=None, customer=None):
        """
        Saves an button infomation
        :param user:
        :param service:
        :param customer:
        :return:
        """
        if user and user.id:
            self.user_id = user.id
        if service and service.id:
            self.service_id = service.id
        if customer and customer.id:
            self.customer_id = customer.id
        db.session.add(self)

        db.session.commit()
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        db.session.commit()


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    wechat_template_id = db.Column(db.String(60))
    wechat_template = db.Column(db.String(500))                                                 # 微信模板内容
    count = db.Column(db.Integer, default=1)                                                    # 数量
    unit = db.Column(db.String(6), default=u'桶')                                                # 单位
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # One-to-Many
    buttons = db.relationship('Button', backref='service',
                              primaryjoin='Button.service_id == Service.id')

    # One-to-Many
    orders = db.relationship('Order', backref='service',
                             primaryjoin='Order.service_id == Service.id')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None):
        """

        :param user:
        :return:
        """
        if user:
            self.user_id = user.id
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        db.session.commit()


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(30))
    addr = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20))
    mobile_phone = db.Column(db.String(15))
    wechat_id = db.Column(db.String(50))

    # One-to-many
    buttons = db.relationship('Button', primaryjoin='Button.customer_id == Customer.id')


    def __init__(self, addr=None):
        self.addr = addr

    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None):
        """

        :param user:
        :return:
        """
        if self.id:
            db.session.add(self)
        else:
            if user:
                self.user_id = user.id
            db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """

        :return:
        """
        db.session.delete(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    button_id = db.Column(db.Integer, db.ForeignKey('buttons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    solved = db.Column(db.Boolean, default=False)


    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, button=None):
        """
        Saves an order and return an order object
        :param button:
        :param user:
        :return: Order object
        """
        if self.id:
            db.session.add(self)
            db.session.commit()
        elif button:
            self.button_id = button.id
            self.user_id = button.user.id
            self.service_id = button.service.id
            db.session.add(self)
            db.session.commit()
        return self

    def delete(self):
        """
        :return:
        """
        db.session.delete(self)
        db.session.commit()


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    #
    # user = User('qitian', '2390saf', '1522351', '15874565462')
    # user.save()
    #
    #
    # user = User.query.filter_by(username='qitian').first()
    # button = Button(node_id='XDF2142314')
    # user.buttons.append(button)
    # user.save()

    # # button.save(user=user)

    # get user buttons
    user = User.query.filter_by(username='qitian').first()
    if user is not None:
        print user.buttons

    # add service
    # service = Service(name=u'马杀鸡一个小时')
    # service.save(user=user)
    #

    # binding button
    service = Service.query.filter_by(name=u'马杀鸡一个小时').first()
    button = Button.query.filter_by(node_id='890087').first()
    if service and button:
        button = button.save(service=service)

    print button.service.name
    print service.buttons[0].node_id

    customer = Customer.query.filter_by(addr=u'南横村59号222房').first()
    # customer.save()
    if customer:
        button.save(customer=customer)
        print 'button binds with customer success!'
    else:
        print 'costomer is None'

    #
    print 'customer.buttons[0].node_id: ' + customer.buttons[0].node_id
    print customer.buttons[1].service.name

    # create an order by node id
    def create_order(node_id):
        order = Order()
        button = Button.query.filter_by(node_id=node_id).first()
        service = button.service

        order.save(button=button)

    order = Order.query.filter_by(button_id=Button.query.filter_by(node_id='890087').first().id).first()
    print 'order service: ', order.service.name



    # customer.delete()
    # customer = Customer(addr=u'南横村59号222房')
    # customer.save(user=user)

    # add buttons
    # button = Button(node_id='111111')
    # user = User.query.filter_by(username='qitian').first()
    # if user is not None:
    #     button.save(user)
    # #
    # #
    # button = Button.query.filter_by(node_id='123456').first()
    # print button.user



    # user.delete()
    # service = Service('hello')
    # button = Button('ffdds189380')
    # customer = Customer('南横村')
    # button.save(user=user, service=service, customer=customer)
