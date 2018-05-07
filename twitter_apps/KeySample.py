def provide_keys(group):
    key = {}
    if group.lower() == 'males':
        # Consumer keys and access tokens, used for OAuth
        key['consumer_key'] = 'vuaBThRequiredConSumer_Key'
        key['consumer_secret'] = 'ThRequiredConSumer_SecReT_Key'
        key['access_token_key'] = '911546456641654-ThRequiredConSumer_ToKeN_Key'
        key['access_token_secret'] = 'ThRequiredConSumer_AcCeSs_ToKen_SecReT_Key'

    elif group.lower() == 'females':
        # Consumer keys and access tokens, used for OAuth
        key['consumer_key'] = 'vuaBThRequiredConSumer_Key'
        key['consumer_secret'] = 'ThRequiredConSumer_SecReT_Key'
        key['access_token_key'] = '911546456641654-ThRequiredConSumer_ToKeN_Key'
        key['access_token_secret'] = 'ThRequiredConSumer_AcCeSs_ToKen_SecReT_Key'

    elif group.lower() == 'liberals':
        # Consumer keys and access tokens, used for OAuth
        key['consumer_key'] = 'vuaBThRequiredConSumer_Key'
        key['consumer_secret'] = 'ThRequiredConSumer_SecReT_Key'
        key['access_token_key'] = '911546456641654-ThRequiredConSumer_ToKeN_Key'
        key['access_token_secret'] = 'ThRequiredConSumer_AcCeSs_ToKen_SecReT_Key'

    elif group.lower() == 'conservatives':
        # Consumer keys and access tokens, used for OAuth
        key['consumer_key'] = 'vuaBThRequiredConSumer_Key'
        key['consumer_secret'] = 'ThRequiredConSumer_SecReT_Key'
        key['access_token_key'] = '911546456641654-ThRequiredConSumer_ToKeN_Key'
        key['access_token_secret'] = 'ThRequiredConSumer_AcCeSs_ToKen_SecReT_Key'

    elif group.lower() == 'logistic':
        # Consumer keys and access tokens, used for OAuth
        key['consumer_key'] = 'vuaBThRequiredConSumer_Key'
        key['consumer_secret'] = 'ThRequiredConSumer_SecReT_Key'
        key['access_token_key'] = '911546456641654-ThRequiredConSumer_ToKeN_Key'
        key['access_token_secret'] = 'ThRequiredConSumer_AcCeSs_ToKen_SecReT_Key'

    return key


def get_password(account):
    if account.lower() == 'femalephv':
        return 'password'
    if account.lower() == 'wsdl':
        return 'password'

    return

