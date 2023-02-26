# 简介

chatgpt确实很好玩。看着也用处很大。所以看到这个东西之后在网上找了觉得合适用的开源的代码。然后自己又有一些特殊的要求，就动手自己改了。

其实我并不太会写python也不会nodejs，我是个只会古老java的上古程序员。这个代码大部分不是自己写的，基本就是抄过来，整合了一下。主要用了两位大佬的：

一个是：

[https://github.com/zhayujie/chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)

大佬做了很好的分层封装，还提供了一个自己的session管理，在一个apikey情况下，做到不同用户独立的会话效果。很赞。
保留内容对应在server目录。

玩了几天，微信被封了。众所周知的原因。

所以寻求web模式的对话。找到了：

[https://github.com/mic1on/chatGPT-web](https://github.com/mic1on/chatGPT-web)

这位大佬做了自己独立的web聊天界面，封装了单独的服务来调用openai。
保留内容对应在web目录。

给两位大佬star。

结合两个项目，我做了一些整合：

- 基于web的聊天界面，脱离微信
- 界面上用户可以起名字，可以设置部分参数
- 增加敏感词，大家懂的
- 后台去掉微信，直接提供web服务

环境是：

node/19.6.0
python 3.9

敏感词库就不上传了。需要的童鞋肯定都能自己找到。词库文件放在

> /server/sen/words

目录下，txt文件即可，可以多个文件，每个词一行。

