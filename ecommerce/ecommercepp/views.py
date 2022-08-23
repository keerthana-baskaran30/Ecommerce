from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from django.http import Http404
from ecommercepp.models import Customer, Product, Cart, Seller
from ecommercepp.serializers import (
    LoginViewSerializer,
    ProductSerializer,
    UserRegisterSerializer,
    DetailCartSerializer,
    SellerAddViewSerializer,
)


def get_function(user_obj, value):
    """Used to get the Seller or Customer object from the respective database tables."""
    if value == "seller":
        try:
            seller_obj = Seller.objects.get(auth_id=user_obj.id)
            return seller_obj
        except Seller.DoesNotExist as exception:
            raise Http404 from exception
    elif value == "customer":
        try:
            cust_obj = Customer.objects.get(auth_id=user_obj.id)
            return cust_obj
        except Customer.DoesNotExist as exception:
            raise Http404 from exception
    return None


class LoginView(generics.GenericAPIView):
    """Used to login a user"""

    permission_classes = [IsAuthenticated]
    serializer_class = LoginViewSerializer

    def get_object(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exception:
            raise Http404 from exception

    def post(self, request):
        user_data = self.get_object(request.user.username)
        serializer = LoginViewSerializer(user_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    """Customer Registration class"""

    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(
            data=request.data, context={"role": "customer"}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                " Customer Registered sucessfully", status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerRegisterView(generics.CreateAPIView):
    """Seller Registration class"""

    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(
            data=request.data, context={"role": "seller"}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                "Seller Registered sucessfully", status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProducts(generics.ListAPIView):
    """Lists out all the products"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DetailProducts(generics.ListAPIView):
    """Displaying a particular product through product id"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        product_id = self.request.query_params.get("pid")
        if product_id is not None:
            queryset = queryset.filter(pid=product_id)
        return queryset


class DetailCategory(generics.ListAPIView):
    """Listing the products based on category"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get("category")
        if category is not None:
            queryset = queryset.filter(pcategory=category)
        return queryset


class SellerAddView(generics.CreateAPIView):
    """Sellers adding the products to the product table"""

    serializer_class = SellerAddViewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_obj = User.objects.get(username=request.user.username)
        seller_obj = get_function(user_obj, "seller")
        serializers = SellerAddViewSerializer(
            data=request.data, context={"seller": seller_obj}
        )
        if serializers.is_valid():
            serializers.save()
            return Response("Product has been Added", status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerUpdateView(generics.UpdateAPIView):
    """Sellers updating the product details in the product table"""

    permission_classes = [IsAuthenticated]
    serializer_class = SellerAddViewSerializer

    def put(self, request):
        user_obj = User.objects.get(username=request.user.username)
        seller_obj = get_function(user_obj, "seller")
        seller_id = seller_obj.id
        pid = self.request.query_params.get("pid")

        if Product.objects.filter(pid=pid).exists():
            product = Product.objects.get(pid=pid)
            if product.seller_id.id == seller_id:
                serializers = SellerAddViewSerializer(product, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response("Product Updated", status=status.HTTP_201_CREATED)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("Product not found", status=status.HTTP_403_FORBIDDEN)
        return Response("Product ID doesnt exists", status=status.HTTP_404_NOT_FOUND)


class SellerDeleteView(generics.DestroyAPIView):
    """Sellers deleting the product through product id"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_obj = User.objects.get(username=request.user.username)
        seller_obj = get_function(user_obj, "seller")
        seller_id = seller_obj.id
        pid = request.query_params.get("pid")
        products = Product.objects.filter(seller_id=seller_id)
        if products.filter(pid=pid).exists():
            Product.objects.get(pid=pid).delete()
            return Response(f"Product {pid} deleted", status=status.HTTP_200_OK)
        return Response("Not found", status=status.HTTP_404_NOT_FOUND)


class SellerDisplayView(generics.ListAPIView):
    """Displaying the products to the sellers"""

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = User.objects.get(username=self.request.user.username)
        seller_obj = get_function(user_obj, "seller")
        seller_id = seller_obj.id
        if seller_id is not None:
            queryset = Product.objects.filter(seller_id=seller_id)
            return queryset
        return None


class CartAddView(generics.CreateAPIView):
    """Adding,incrementing and decrementing products to the customer cart"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_obj = User.objects.get(username=self.request.user.username)
        cust_obj = get_function(user_obj, "customer")
        cust_id = cust_obj.id
        pid = request.query_params.get("pid")
        qty = request.query_params.get("qty")
        if cust_id is not None and pid is not None:
            if Product.objects.filter(pid=pid).exists():
                product = Product.objects.get(pid=pid)
                if Cart.objects.filter(cust_id=cust_id).exists():
                    cart_value = Cart.objects.get(cust_id=cust_id)
                    if pid in cart_value.cart_item:
                        try:
                            qty_value = cart_value.cart_item[pid]["pqty"] + int(qty)
                        except ValueError as exception:
                            return Response(f"Value error: {exception}")
                        if qty_value > 0:
                            cart_value.cart_item[pid]["pqty"] = qty_value
                            cart_value.save()
                            return Response("Updated", status=status.HTTP_200_OK)
                        if qty_value <= 0:
                            del cart_value.cart_item[pid]
                            cart_value.save()
                            if cart_value.cart_item == {}:
                                Cart.objects.get(cust_id=cust_id).delete()
                                return Response(
                                    "No items in the cart", status=status.HTTP_200_OK
                                )
                            return Response("Item removed", status=status.HTTP_200_OK)
                    else:
                        if int(qty) <= 0:
                            return Response("Negative quantity")
                        cart_value.cart_item[pid] = {
                            "pid": pid,
                            "pname": product.pname,
                            "pdescription": product.pdescription,
                            "pprice": product.pprice,
                            "pcategory": product.pcategory,
                            "pqty": int(qty),
                        }
                        cart_value.save()
                        return Response("added", status=status.HTTP_201_CREATED)
                else:
                    if int(qty) <= 0:
                        return Response("Negative quantity")
                    cart_item = {
                        pid: {
                            "pid": pid,
                            "pname": product.pname,
                            "pdescription": product.pdescription,
                            "pprice": product.pprice,
                            "pcategory": product.pcategory,
                            "pqty": int(qty),
                        }
                    }
                    Cart.objects.create(cust_id=cust_obj, cart_item=cart_item).save()
                    return Response("Added", status=status.HTTP_201_CREATED)
        return Response("Invalid details", status=status.HTTP_400_BAD_REQUEST)


# viewing the cart
class DetailCart(generics.ListAPIView):
    """Displaying the customer carts through customer id"""

    serializer_class = DetailCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_obj = User.objects.get(username=self.request.user.username)
        cust_obj = get_function(user_obj, "customer")
        cust_id = cust_obj.id
        if cust_id is not None:
            queryset = Cart.objects.filter(cust_id=cust_id)
        return queryset


# Deleteing the item from the cart
class DeleteCartView(generics.DestroyAPIView):
    """Deleting the products in the customer cart"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_obj = User.objects.get(username=self.request.user.username)
        cust_obj = get_function(user_obj, "customer")
        cust_id = cust_obj.id
        pid = request.query_params.get("pid")
        if cust_id is not None and pid is not None:
            if Product.objects.filter(pid=pid).exists():
                if Cart.objects.filter(cust_id=cust_id).exists():
                    cart_value = Cart.objects.get(cust_id=cust_id)
                    if pid in cart_value.cart_item:
                        del cart_value.cart_item[pid]
                        cart_value.save()
                        if cart_value.cart_item == {}:
                            Cart.objects.get(cust_id=cust_id).delete()
                            return Response("Deleted", status=status.HTTP_200_OK)
                        return Response("Deleted", status=status.HTTP_200_OK)
                    return Response(
                        "Not found in the cart", status=status.HTTP_404_NOT_FOUND
                    )
                return Response("Cart is Empty", status=status.HTTP_400_BAD_REQUEST)
            return Response("Invalid product ID", status=status.HTTP_404_NOT_FOUND )
        return Response(
            "invalid product id or customer id", status=status.HTTP_400_BAD_REQUEST
        )
