# encoding:utf-8

import config
from common.log import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sen.DFA import DFAFilter
from bridge.bridge import Bridge

from model import Message

#初始化过滤器
gfw = DFAFilter()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/completions.do")
async def completions(request: Request, message: Message):
    # Message的结构是兼容向openai发请求的，其中prompt是用户发来的文本
    # 这里先做敏感词过滤
    content = message.dict().get("prompt")
    
    sen = gfw.check(content)
    if len(sen) > 0:
        logger.debug("[check sen] new_query={},sen={}".format(content,sen))
        res = {"choices": [
                {"text":config.conf().get("sen_reply")}]
        }
    else:
        # 这里Bridge默认用openai
        #TODO: 后续根据用户发送的指令 井号开头表示指令，切换机器人，这里只处理切换机器人指令
        #更多指令，比如清空记忆，都放在机器人本身去处理
        #接受5个参数，一个是用户的提问，一个是用户id，以及max_tokens,temperature,top_p,后三个可以为空
        context = dict()
        context['from_user_id'] = message.dict().get("user_id")
        context['max_tokens'] = message.dict().get("max_tokens")
        context['temperature'] = message.dict().get("temperature")
        context['top_p'] = message.dict().get("top_p")
        reply = Bridge().fetch_reply_content(content, context)
        res = {"choices": [
                {"text":reply}]
        }
    return res


@app.get("/credit_summary.do")
async def credit_summary(request: Request):
    #api_key = request.headers.get('api_key')
    #res = await api.credit_summary(api_key=api_key)
    res = Bridge().credit_summary()
    return res


if __name__ == '__main__':
    import uvicorn
    
    # load config
    config.load_config()

    uvicorn.run("app:app", host="0.0.0.0", port=8000)
