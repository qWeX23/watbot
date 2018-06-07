from api_helpers import strawpoll

#Tests
poll1="question ? poll answer test"
poll2="question asf asf asf asf ewg gwejjjjjjjjj questoin? poll saasfnlkn test"
# 
def parse_poll(poll):
    found_question = False
    question = ''
    answers=[]
    for word in poll:
        if not found_question:
            question += ' ' + word
        else:
            answers.append(word)
        if '?' in word:
            found_question = True
    if found_question:
        return (question,answers)
    else:
        return None

async def make_poll(args, client=None):
    poll = parse_poll(args)
    if poll:
        return strawpoll.get_poll_url(strawpoll.make_poll(poll[0],poll[1])['id'])
    else:
        return "correct usage: !watbot poll Your Question? answer answer answer ..."

#test
if __name__ == "__main__":
    print(parse_poll(poll1))
    print(parse_poll(poll2))
