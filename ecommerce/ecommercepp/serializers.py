import re
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from ecommercepp.models import Product, Cart, Customer, Seller


# login
class LoginViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name"]


# register
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    phone = serializers.CharField(max_length=10)

    sex = serializers.CharField(max_length=1)
    address = serializers.CharField(max_length=5000)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone",
            "sex",
            "address",
        ]

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        # print(user)
        if self.context["role"] == "customer":
            Customer.objects.create(
                auth_id=user,
                phone=validated_data["phone"],
                sex=validated_data["sex"],
                address=validated_data["address"],
            )
        elif self.context["role"] == "seller":
            Seller.objects.create(
                auth_id=user,
                phone=validated_data["phone"],
                sex=validated_data["sex"],
                address=validated_data["address"],
            )
        return user

    # def create(self, validated_data):
    #     if self.context["role"] == "customer":
    #         user = Customer.objects.create(
    #             first_name=validated_data["first_name"],
    #             last_name=validated_data["last_name"],
    #             username=validated_data["username"],
    #             email=validated_data["email"],
    #             phone=validated_data["phone"],
    #             sex=validated_data["sex"],
    #             address=validated_data["address"],
    #         )
    #         user.set_password(validated_data["password"])
    #         user.save()

    #     elif self.context["role"] == "seller":
    #         user = Seller.objects.create(
    #             first_name=validated_data["first_name"],
    #             last_name=validated_data["last_name"],
    #             username=validated_data["username"],
    #             email=validated_data["email"],
    #             phone=validated_data["phone"],
    #             sex=validated_data["sex"],
    #             address=validated_data["address"],
    #         )
    #         user.set_password(validated_data["password"])
    #         user.save()
    #     return user

    def validate(self, attrs):
        pattern = re.compile("^([9876])[0-9]{9}$")

        try:
            if not bool(re.fullmatch("[A-Za-z]{2,25}", attrs["first_name"])):
                raise serializers.ValidationError("firstname field is invalid")

            if not bool(re.fullmatch("[A-Za-z]{2,25}", attrs["last_name"])):
                raise serializers.ValidationError("lastname field is invalid")

            if not bool(re.fullmatch("([a-zA-Z0-9._@-]{2,20})", attrs["username"])):
                raise serializers.ValidationError("Enter a valid username")
            if not bool(
                re.fullmatch(
                    r"([a-zA-Z0-9]{5,20})+@([a-zA-Z]{3,5})+\.([a-zA-Z\.]{3,10})$",
                    attrs["email"],
                )
            ):
                raise serializers.ValidationError("Enter a valid email")

            if self.context["role"] == "customer":
                if Customer.objects.filter(phone=attrs["phone"]).exists():
                    raise serializers.ValidationError("Phone number already exists.")
                if not pattern.match(attrs["phone"]):
                    raise serializers.ValidationError("Phone number is invalid.")

            if self.context["role"] == "seller":
                if Seller.objects.filter(phone=attrs["phone"]).exists():
                    raise serializers.ValidationError("Phone number already exists.")
                if not pattern.match(attrs["phone"]):
                    raise serializers.ValidationError("Phone number is invalid.")

            if attrs["sex"].lower() not in "mf":
                raise serializers.ValidationError("Field is invalid")

            if not bool(re.fullmatch(r"^[a-zA-Z0-9\s.,/]+$", attrs["address"])):
                raise serializers.ValidationError("Address field is invalid")

            return attrs

        except KeyError as e:
            raise serializers.ValidationError(f"Key error : {e}")

       
# Displaying products
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product


# Seller add
class SellerAddViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["seller_id"]

    def create(self, validated_data):
        sellerobj = self.context

        pdt = Product.objects.create(
            pid=validated_data["pid"],
            pname=validated_data["pname"],
            pdescription=validated_data["pdescription"],
            pprice=validated_data["pprice"],
            pcategory=validated_data["pcategory"],
            seller_id=sellerobj["seller"],
        )
        # pdt.save()
        return pdt

    def update(self, instance, validated_data):
        instance.pid = validated_data.get("pid", instance.pid)
        instance.pname = validated_data.get("pname", instance.pname)
        instance.pdescription = validated_data.get(
            "pdescription", instance.pdescription
        )
        instance.pprice = validated_data.get("pprice", instance.pprice)
        instance.pcategory = validated_data.get("pcategory", instance.pcategory)
        instance.save()
        return instance

    def validate(self, attrs):
        if not bool(re.fullmatch("^[a-zA-Z0-9]+$", attrs["pid"])):
            raise serializers.ValidationError("PID is invalid")

        if not bool(re.fullmatch(r"^[a-zA-Z0-9_.\s]+$", attrs["pname"])):
            raise serializers.ValidationError("product name field is invalid")

        if not bool(re.fullmatch(r"^[a-zA-Z0-9\s._:;<>,/()${}]+$", attrs["pdescription"])):
            raise serializers.ValidationError(" Description is invalid")

        if not bool(re.fullmatch(r"^[a-zA-Z0-9\s]+$", attrs["pcategory"])):
            raise serializers.ValidationError("product category is invalid")

        return attrs


# diaplying the cart
class DetailCartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart
