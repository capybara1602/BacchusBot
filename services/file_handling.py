#import sys
#sys.path.append("C:/Users/marar/Рабочий стол/IT/python/тг_бот/код/lexicon")
#from lexicon import LEXICON

def prepare_book(inf: str) -> None:

    book: dict[str, str] = {}

    with open(inf, 'r', encoding='utf-8') as file:
        st1 = ''
        st2 = ''
        for i in file.readlines():
    
            if i[0] == "\"":
                i = i.replace('"','').strip('\n')
                st1 = i
                
            elif len(i.strip()) != 0 and i[0] != "\"":
                #i = i.strip('\n')
                st2 += i
                

            elif len(i.strip()) == 0:
                book[st1] = st2
                st1 = ''
                st2 = ''
    return book

inf = "inf.txt"

book = prepare_book(inf)


            
