import random
import os

agent_file = os.path.dirname(os.path.abspath(__file__)) + "/user-agents"

def fake_agent():
    fakeaagent = None
    with open(agent_file) as f:
        a = f.readlines()
        random.shuffle(a)
        fakeaagent = a[0].replace("\n","")
    return fakeaagent

if __name__ == '__main__':
    print(fake_agent())