from app.api.v2.database import DatabaseConnection, conn, cur, save
from werkzeug.security import generate_password_hash


class UserModels(DatabaseConnection):
    
    def __init__(self, name, email, username, password, admin):
        super().__init__()
        self.name = name
        self.email = email
        self.username = username
        if password:
            self.password = generate_password_hash(password)
        self.admin = admin

    def Users_table(self):
        ''' create table for users '''
        cur.execute(
            '''
            CREATE TABLE IF NOT EXIST public."Users"
            (
                user_id integer NOT NULL DEFAULT nextval('"Users_user_id_seq"'::regclass),
                name "char" NOT NULL,
                email "char" NOT NULL,
                username "char" NOT NULL,
                password "char" NOT NULL,
                CONSTRAINT "Users_pkey" PRIMARY KEY (user_id),
                CONSTRAINT "unique email" UNIQUE (email)
            )
            '''
        )
        save(conn)
        

    def add_users(self):
        ''' add user to the users table'''
        cur.execute(
            """
            INSERT INTO users(name, email, username, password, admin)
            VALUES(%s, %s, %s, %s, %s)
            """,
            (self.name, self.email, self.username,
             self.password, self.admin)
        )
        save(conn)

    def fetch_by_email(self, email):
        ''' fetch user by email '''
        cur.execute(
            "SELECT * FROM Users WHERE email=%s", (email)
        )

        user = cur.fetchone()

        save(conn)

        if user:
            return user
        return None

    def count_users(self):
        """ count all existing users """
        cur.execute("SELECT COUNT(*) FROM Users")
        users = cur.fetchall()

        save(conn)

        if users:
            return users
        return None

    def all_users(self):
        """ count all existing users """
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()

        save(conn)

        if users:
            return users
        return None


    def serialize(self):
        return dict(
            name = self.name,
            email = self.email,
            username = self.username,
            password = self.password,
            admin = self.admin
        )


class FoodModels(DatabaseConnection):
    
    def __init__(self, name, price, image, added_by, edited_by):
        super().__init__()
        self.name = name
        self.price = price
        self.image = image
        self.added_by = added_by
        self.edited_by = edited_by
        

    def Foods_table(self):
        ''' create foods table '''
        cur.execute(
            '''
            CREATE TABLE IF NOT EXIST public."Foods"
            (
                food_id integer NOT NULL DEFAULT nextval('"Foods_food_id_seq"'::regclass),
                food_name "char" NOT NULL,
                price money NOT NULL,
                image "char" NOT NULL,
                created_by integer NOT NULL,
                editted_by integer,
                CONSTRAINT "Foods_pkey" PRIMARY KEY (food_id),
                CONSTRAINT "unique food" UNIQUE (food_id)
            )
            '''
        )
        save(conn)

    def add_foods(self):
        ''' add food items to the foods table'''
        cur.execute(
            """
            INSERT INTO Foods(name, price, image, added_by, edited_by)
            VALUES(%s, %i, %s, %i, %i)
            """,
            (self.name, self.price, self.image, self.added_by, self.edited_by)
        )
        save(conn)
        
    def get_by_id(self, food_id):
        ''' fetch food by id '''
        cur.execute(
            "SELECT * FROM Foods WHERE id=%s", (food_id)
        )

        food = cur.fetchone()

        save(conn)

        if food:
            return food
        return None

    def get_price_by_id(self, food_id):
        ''' fetch food by id '''
        cur.execute(
            "SELECT price FROM Foods WHERE id=%s", (food_id)
        )

        food = cur.fetchone()

        save(conn)

        if food:
            return food
        return None
        
    def get_all(self):
        """ fetch all available food items """
        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()

        save(conn)

        if foods:
            return foods
        return None


    def update_food(self, food_id):
        ''' update a food item '''
        cur.execute("""UPDATE Foods
            SET price = %i,
                image = %s ,
                edited_by = %i
            WHERE
            food_id = %i""", 
            (self.price, self.image, self.edited_by, food_id)
            )

        save(conn)


    def delete_food(self, food_id):
        ''' delete a food item '''
        cur.execute("DELETE FROM Foods WHERE id=%i", (food_id))

        save(conn)
    
    def serialize(self):
        return dict(
            name = self.name,
            price = self.price,
            image = self.image,
            added_by = self.added_by,
            edited_by = self.edited_by
        )


class OrderModels(DatabaseConnection):

    def __init__(self, payment_mode, status, destination, grand_total, number_of_items, ordered_by, updated_by, food_id, quantity, total):
        super().__init__()
        self.payment_mode = payment_mode
        self.status = status
        self.destination = destination
        self.grand_total = grand_total
        self.number_of_items = number_of_items
        self.ordered_by = ordered_by
        self.updated_by = updated_by
        self.food_id = food_id
        self.quantity = quantity
        self.total = total
        self.price = FoodModels.get_price_by_id(self, food_id)

    def Orders_table(self):
        ''' create orders table '''
        cur.execute(
            '''
            CREATE TABLE IF NOT EXIST public."Orders"
            (
                order_id integer NOT NULL DEFAULT nextval('"Orders_order_id_seq"'::regclass),
                payment_mode "char" NOT NULL,
                status "char" NOT NULL,
                grand_total money NOT NULL,
                number_of_items integer NOT NULL,
                ordered_by integer NOT NULL,
                updated_by integer NOT NULL,
                destination "char" NOT NULL,
                CONSTRAINT "Orders_pkey" PRIMARY KEY (order_id)
            )
            '''
        )
        save(conn)

    def Orders_Items_table(self):
        ''' create orders table '''
        cur.execute(
            '''
            CREATE TABLE IF NOT EXIST public."Order_Items"
            (
                order_item_id integer NOT NULL DEFAULT nextval('"Order_Items_order_item_id_seq"'::regclass),
                food_id integer NOT NULL,
                order_id integer NOT NULL,
                quantity integer NOT NULL,
                price money NOT NULL,
                total money NOT NULL,
                CONSTRAINT "Order_Items_pkey" PRIMARY KEY (order_item_id)
            )'''
        )
        save(conn)

    def add_order(self):
        ''' add orders to the orders table'''
        cur.execute("""
            INSERT INTO Orders(payment_mode, destination, status, ordered_by, grand_total, number_of_items, updated_by)
            VALUES(%s, %s, %s, %i, %i, %i, %i)
            """,
            (self.payment_mode, self.destination, self.status, self.ordered_by, self.grand_total, self.number_of_items, self.updated_by)
        )
        save(conn)
            
    def add_order_items(self):
        ''' add Order Items to the Order Items table'''
        cur.execute("""
            INSERT INTO Order_Items(food_id, order_id, quantity, price, total)
            VALUES(%i, %i, %i, %i)
            """,
            (self.food_id, OrderModels.last_order_id(self), self.quantity, self.price, self.total)
        )
        save(conn) 

    def last_order_id(self):
        """ fetch the latest order in orders """
        cur.execute("SELECT * FROM Orders ORDER BY id DESC LIMIT 1")
        orders = cur.fetchall()

        save(conn)

        if orders:
            orders = int(orders)+1
            return orders
        else:
            return 1

    def get_all(self):
        """ fetch all available orders """
        cur.execute("SELECT * FROM Orders")
        orders = cur.fetchall()

        save(conn)

        if orders:
            return orders
        return None

    def get_by_id(self, order_id):
        ''' fetch order by ID '''
        cur.execute(
            "SELECT * FROM Orders WHERE id=%s", (order_id)
        )

        order = cur.fetchone()

        save(conn)

        if order:
            return order
        return None
    
    def update_order(self, order_id):
        ''' update a order status '''
        cur.execute("""UPDATE Orders
            SET status = %s,
                updated_by = %i
            WHERE
            order_id = %i""", 
            (self.status, self.updated_by, order_id)
            )

        save(conn)
        
    def serialize_order(self):
        return dict(
            payment_mode = self.payment_mode,
            destination = self.destination,
            status = self.status,
            ordered_by = self.ordered_by,
            grand_total = self.grand_total,
            number_of_items = self.number_of_items,
            updated_by = self.updated_by
        )

    def serialize_order_items(self):
        return dict(
            food_id = self.food_id,
            order_id = OrderModels.last_order_id(self),
            quantity = self.quantity,
            price = self.price,
            total = self.total
        )

