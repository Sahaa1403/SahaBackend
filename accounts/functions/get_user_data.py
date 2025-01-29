def get_normal_user_data(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "email": user.email,
    }


def get_producer_user_data(user):

    #if user.petshop_profile.national_card:
        #national_card = user.petshop_profile.national_card.url
    #else:
        #national_card = None

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
    }


def get_user_data(user):
    if user.user_type == "normal":
        return get_normal_user_data(user)
    if user.user_type == "producer":
        return get_producer_user_data(user)
