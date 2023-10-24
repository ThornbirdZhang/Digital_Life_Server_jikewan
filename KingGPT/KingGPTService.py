import logging
import os
import time
import requests

#import KingGPT.machine_id
#import KingGPT.tune as tune


class KingGPTService():
    def __init__(self, args):
        logging.info('Initializing KingGPT Service...')
        #self.chatVer = args['chatVer']
        self.chatVer = args.chatVer

        #self.tune = tune.get_tune(args.character, args.model)

        self.counter = 0

        #self.brainwash = args['brainwash']
        self.brainwash = args.brainwash

        logging.info('KingGpt API Chatbot initialized.')

    def ask(self, text):
        stime = time.time()
        #request to king gpt.
        url = "http://43.240.1.174:7861/chat/knowledge_base_chat"
        request_body = {
            "query": "必须在20个汉字内回答，你是谁？",
            "knowledge_base_name": "Charles",
            "top_k": 3,
            "score_threshold": 1,
            "history": [],
            "stream": False,
            "model_name": "llama-2-7b-chat-hf",
            "temperature": 0.7,
            "local_doc_url": False
        }

        response = requests.post(url, json=request_body)
        data = response.json()
        prev_text = data["answer"]

        logging.info('ChatGPT Response: %s, time used %.2f' % (prev_text, time.time() - stime))
        return prev_text

    #TODO 
    def ask_stream(self, text):
        prev_text = ""
        complete_text = ""
        stime = time.time()
        if self.counter % 5 == 0 and self.chatVer == 1:
            if self.brainwash:
                logging.info('Brainwash mode activated, reinforce the tune.')
            else:
                logging.info('Injecting tunes')
            asktext = self.tune + '\n' + text
        else:
            asktext = text
        self.counter += 1
        for data in self.chatbot.ask(asktext) if self.chatVer == 1 else self.chatbot.ask_stream(text):
            message = data["message"][len(prev_text):] if self.chatVer == 1 else data

            if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                complete_text += message
                logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
                yield complete_text.strip()
                complete_text = ""
            else:
                complete_text += message

            prev_text = data["message"] if self.chatVer == 1 else data

        if complete_text.strip():
            logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
            yield complete_text.strip()

if __name__ == '__main__':
    arg = {}
    arg['chatVer'] = 1
    arg['brainwash'] = False
    gpt = KingGPTService(arg)
    answer = gpt.ask("who is it?")
    print(f"kingGpt return: {answer}")