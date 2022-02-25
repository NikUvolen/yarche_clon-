import pprint
import re


def split_string(my_string) -> list:
    result = []
    my_string = my_string.split('\n')
    message = ''
    for line in my_string:
        if line == '':
            result.append(message)
            message = ''
        else:
            message += line
    else:
        result.append(message)

    return result


def find_suitable_vacancy(parse_string: list) -> int:
    for num, message in enumerate(parse_string[3:]):
        pprint.pprint(message)
        employment = re.findall(r'./.', message)
        time = re.findall(r'\(.*?\)', message)
        if employment and time:
            employment = employment[0][0]
            time = time[0]
            search_time_ = re.search(r'\d+', time)
            if search_time_:
                time = time[search_time_.start():search_time_.end()]

                print(employment)
                print(time)

                if employment == '0' and int(time) > 6:
                    return num + 1
    else:
        return False

