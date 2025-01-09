from fastapi import HTTPException
from sqlalchemy.orm import Session
# Import the ShoppingCart and ShoppingCartItem classes from the models module
from models.models import ShoppingCart, ShoppingCartItem, Product, CartAdjustment
from utils.card_Settings import Settings

class CartService:
    @staticmethod
    def get_cart(customer_id, db: Session):
        '''
        This function retrieves the cart of a customer from the database.

        Parameters:
        - customer_id: the ID of the customer whose cart will be retrieved.

        Returns:
        - a dictionary with the key "cart" and a list of dictionaries representing the items in the cart.
        '''
        # Query the database to get the cart of the customer with the given customer_id
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()

        if not cart:
            return {"cart": []}
        
        # Query the database to get the items in the cart
        items = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id).all()
        # Return a list of dictionaries representing the items in the cart
        return {"cart": [{"product_id": item.product_id, "quantity": item.quantity} for item in items]}


    @staticmethod
    def add_item_to_persistent_cart(cart_item, customer_id, db: Session):
        '''
        This function adds an item to the persistent cart of a customer in the database.
        If the customer does not have an active cart, a new cart is created for the customer.

        Parameters:
        - cart_item: an instance of the CartItem class which is a Pydantic model representing the item to be added to the cart.
            - cart_item.product_id: the ID of the product to be added.
            - cart_item.quantity: the quantity of the product to be added.
        - customer_id: the ID of the customer whose cart the item will be added to.
        
        Returns:
        - a dictionary with the key "message" and a string value indicating that the item has been added to the cart.
        '''

        print("Iyiyiz")
        # Check if the customer has an active cart
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        # If not, create a new cart
        if not cart:
            # create a new instance of the ShoppingCart class (which is the mapping of the shoppingcart table in the database)
            cart = ShoppingCart(customer_id=customer_id, cart_status="active")
            db.add(cart)
            db.commit()
            # add the cart to the database, then commit the transaction, and refresh the cart object to get the updated cart_id
            db.refresh(cart)

        # Check if the item is already in the cart
        existing_item = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id, ShoppingCartItem.product_id == cart_item.product_id).first()
        print("Iyiyiz2")
        # find the product in db
        product = db.query(Product).filter(Product.product_id == cart_item.product_id).first()

        if existing_item:
            if product.quantity < cart_item.quantity + existing_item.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")
            else:
                existing_item.quantity += cart_item.quantity
        else:
            # If the item is not in the cart, check if the quantity of the product is enough
            if product.quantity < cart_item.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")
            else:
                # If there is enough stock, create a new instance of the ShoppingCartItem class (which is the mapping of the shoppingcart_item table in the database)
                new_cart_item = ShoppingCartItem(cart_id=cart.cart_id, product_id=cart_item.product_id, quantity=cart_item.quantity)
                # add the new item to the database
                db.add(new_cart_item)


        db.commit()
        return {"message": "Item added to the persistent cart."}

    @staticmethod
    def merge_session_cart_with_persistent_cart(items, customer_id, db: Session):
        '''
        This function merges a session-based cart with the persistent cart of a customer in the database.

        Parameters:
        - items: a list of instances of the CartItem class which is a Pydantic model representing the items to be added to the cart.
            - cart_item.product_id: the ID of the product to be added.
            - cart_item.quantity: the quantity of the product to be added.
        - customer_id: the ID of the customer whose cart the items will be added to.

        Returns:
        - a dictionary with the key "message" and a string value indicating that the session cart has been merged with the persistent cart.
        '''
        
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        # if the customer does not have an active cart, create a new cart and add it to db, commit, refresh 
        if not cart:
            cart = ShoppingCart(customer_id=customer_id, cart_status="active")
            db.add(cart)
            db.commit()
            db.refresh(cart)
        # for each item in the items list, check if the item is already in the cart (for example, user can add somethign to their shopping list without logging in, once they logged in we need to merge it with the existing one.)
        for item in items:
            existing_item = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id, ShoppingCartItem.product_id == item.product_id).first()
            if existing_item:
                existing_item.quantity += item.quantity
            else:
                # creating a new instance of the ShoppingCartItem class which is the mapping of the shoppingcart_item table in the database
                new_cart_item = ShoppingCartItem(cart_id=cart.cart_id, product_id=item.product_id, quantity=item.quantity)
                # add this ShoppingCartItem to the database
                db.add(new_cart_item)

        db.commit()
        return {"message": "Session cart merged with persistent cart."}

    @staticmethod
    def remove_item_from_cart(product_id, customer_id, db: Session):
        '''
        This function removes an item from the persistent cart of a customer in the database.

        Parameters:
        - product_id: the ID of the product to be removed from the cart.
        - customer_id: the ID of the customer whose cart the item will be removed from.
        - db: the database session.

        Returns:
        - a dictionary with the key "message" and a string value indicating that the item has been removed from the cart.
        '''
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id, ShoppingCartItem.product_id == product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        db.delete(item)
        db.commit()
        return {"message": "Item removed from the cart"}

    # function to decrease the quantity of an item by 1 in the cart (if the quantity is already 1, remove the item)
    @staticmethod
    def decrease_item_quantity(product_id, customer_id, db: Session):
        '''
        This function decreases the quantity of an item in the persistent cart of a customer in the database.
        If item quantity is already 1, the item is removed from the cart.

        Parameters:
        - product_id: the ID of the product whose quantity will be decreased in the cart.
        - customer_id: the ID of the customer whose cart the item is in.
        - db: the database session.

        Returns:
        - a dictionary with the key "message" and a string value indicating that the item quantity has been decreased in the cart.
        '''
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id, ShoppingCartItem.product_id == product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.delete(item)
        db.commit()
        return {"message": "Item quantity decreased in the cart"}

    # function to increase the quantity of an item by 1 in the cart (maybe needed for the frontend later)
    @staticmethod
    def increase_item_quantity(product_id, customer_id, db: Session):
        '''
        This function increases the quantity of an item in the persistent cart of a customer in the database.

        Parameters:
        - product_id: the ID of the product whose quantity will be increased in the cart.
        - customer_id: the ID of the customer whose cart the item is in.
        - db: the database session.

        Returns:
        - a dictionary with the key "message" and a string value indicating that the item quantity has been increased in the cart.
        '''
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id, ShoppingCartItem.product_id == product_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product.quantity >= item.quantity + 1:
            item.quantity += 1
        
        db.commit()
        return {"message": "Item quantity increased in the cart"}


    # function to clear the cart of a customer
    @staticmethod
    def clear_cart(customer_id, db: Session):
        '''
        This function clears the cart of a customer in the database. However, it does not delete the cart itself. It
        remains as active in the shopping card table. 

        Parameters:
        - customer_id: the ID of the customer whose cart will be cleared.
        - db: the database session.

        Returns:
        - a dictionary with the key "message" and a string value indicating that the cart has been cleared.
        '''
        # it clears the first active cart of the customer
        cart = db.query(ShoppingCart).filter(ShoppingCart.customer_id == customer_id, ShoppingCart.cart_status == "active").first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        items = db.query(ShoppingCartItem).filter(ShoppingCartItem.cart_id == cart.cart_id).all()
        for item in items:
            db.delete(item)
        db.commit()
        return {"message": "Cart cleared"}


'''
- Total Cost Calculation -> when we have the products table, we can calculate the total cost of the items in the cart.
- Detailed Cart Item View: Expand the get_cart method to return more detailed information about each item, such as the product name, price, description, and image URL
- applying discount to the cart when we have the discount table
- Cart Expiry maybe?
- Custom Sorting Options: Allow users to view and sort items in the cart (e.g., by price, popularity, etc.), which can be handy for larger shopping lists.
-  Add a prepare_checkout endpoint that checks for item availability and locks stock temporarily to prevent overselling.
'''
