def get_contract_abi(abi_json):
    import os
    from alldio.settings import STATIC_METASITE
    abi_path = os.path.join(STATIC_METASITE, abi_json)
    f = open(abi_path, 'r')
    abi = ''
    for i in f.readlines():
        abi += i.replace('\n', '').replace(' ', '')
    return abi
