# encoding:utf-8

from bot.bot import Bot
from config import conf
from common.log import logger
import time
import requests
import json

user_session = dict()

# yuan模型，对接本机127.0.0.0:19999服务
class YuanBot(Bot):

    def reply(self, query, context=None):

        # acquire reply content
        if not context or not context.get('type') or context.get('type') == 'TEXT':
            logger.info("[YUAN] query={}".format(query))
            from_user_id = context['from_user_id']
            if query == '#清除记忆':
                Session.clear_session(from_user_id)
                return '记忆已清除'

            new_query = Session.build_session_query(query, from_user_id)
            logger.debug("[YUAN] session query={}".format(new_query))

            reply_content = self.reply_text(new_query, from_user_id, 0)
            logger.debug("[YUAN] new_query={}, user={}, reply_cont={}".format(new_query, from_user_id, reply_content))
            if reply_content and query:
                Session.save_session(query, reply_content, from_user_id)
            return reply_content

        elif context.get('type', None) == 'IMAGE_CREATE':
            return '不支持图片'

    def reply_text(self, query, user_id, retry_count=0):
        try:
            #发送http请求获取回答
            headers = {'Content-Type': 'application/json'}
            query = {'q':query}
            response = requests.post(url='127.0.0.1:19999', headers=headers, data=json.dumps(query))
            res = json.loads(response.text)
            uuid = res.get('uuid')
            res_content = res.get('answer')
            logger.info("[YUAN] reply={}".format(res_content))
            return res_content
        except Exception as e:
            # unknown exception
            logger.exception(e)
            Session.clear_session(user_id)
            return "请再问我一次吧"

class Session(object):
    @staticmethod
    def build_session_query(query, user_id):
        '''
        build query with conversation history
        e.g.  Q: xxx
              A: xxx
              Q: xxx
        :param query: query content
        :param user_id: from user id
        :return: query content with conversaction
        '''
        prompt = conf().get("character_desc", "")
        if prompt:
            prompt += "\n\n"
        session = user_session.get(user_id, None)
        if session:
            for conversation in session:
                prompt += "Q: " + conversation["question"] + "\n\n\nA: " + conversation["answer"] + "<|im_end|>\n"
            prompt += "Q: " + query + "\nA: "
            return prompt
        else:
            return prompt + "Q: " + query + "\nA: "

    @staticmethod
    def save_session(query, answer, user_id):
        max_tokens = conf().get("conversation_max_tokens")
        if not max_tokens:
            # default 3000
            max_tokens = 1000
        conversation = dict()
        conversation["question"] = query
        conversation["answer"] = answer
        session = user_session.get(user_id)
        logger.debug(conversation)
        logger.debug(session)
        if session:
            # append conversation
            session.append(conversation)
        else:
            # create session
            queue = list()
            queue.append(conversation)
            user_session[user_id] = queue

        # discard exceed limit conversation
        Session.discard_exceed_conversation(user_session[user_id], max_tokens)


    @staticmethod
    def discard_exceed_conversation(session, max_tokens):
        count = 0
        count_list = list()
        for i in range(len(session)-1, -1, -1):
            # count tokens of conversation list
            history_conv = session[i]
            count += len(history_conv["question"]) + len(history_conv["answer"])
            count_list.append(count)

        for c in count_list:
            if c > max_tokens:
                # pop first conversation
                session.pop(0)

    @staticmethod
    def clear_session(user_id):
        user_session[user_id] = []
