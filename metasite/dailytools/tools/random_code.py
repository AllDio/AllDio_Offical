def get_random_code():
    import random
    code_list = [chr(i) for i in range(48,58)] + [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)]
    random_code = ''
    for i in range(16):
        random_code += code_list[random.choice(range(len(code_list)))][0]
        if (i+1)%4 == 0 and i != 0 and i != 15:
            random_code += '-'
    return random_code


def get_random_code_32():
    import random
    code_list = [chr(i) for i in range(48,58)] + [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)]
    random_code = ''
    for i in range(32):
        random_code += code_list[random.choice(range(len(code_list)))][0]
        if (i+1)%4 == 0 and i != 0 and i != 31:
            random_code += '-'
    return random_code

# codes = []
# for i in range(150):
#     code = get_random_code()
#     while code in codes:
#         code = get_random_code_32()
#     codes.append(code)
# [i for i in codes if print(i)]

