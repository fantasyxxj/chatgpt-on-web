<script setup lang="ts">
import dayjs from 'dayjs'
import { ClearOutlined, LoadingOutlined, RedoOutlined, UserOutlined, SettingOutlined } from '@ant-design/icons-vue'
import { useStorage } from '@vueuse/core'
import { completion, creditSummary } from '@/api'
import Message from './components/message.vue'

const createdAt = dayjs().format('YYYY-MM-DD HH:mm:ss')
const loadding = ref(false)
const visibleName = ref(false)
const visiblePara = ref(false)
const summary = ref({} as any)

const message = ref('')
const user_id = useStorage('user_id', '')
const messages = useStorage('messages', [
  {
    username: "chatGPT",
    msg: "Hello, I'm chatGPT",
    time: dayjs().format('HH:mm'),
    type: 0,
  },
])

const max_tokens = useStorage('max_tokens',512)
const temperature = useStorage('temperature',1)
const top_p = useStorage('top_p',1)

const sendMessage = async () => {
  loadding.value = true
  const text = message.value
  message.value = ""
  messages.value.push({
    username: "user",
    msg: text,
    time: dayjs().format('HH:mm'),
    type: 1,
  })

  const data: any = await completion(text)


  const replyMessage = data?.choices ? data.choices[0].text : data?.error?.message
  messages.value.push({
    username: "chatGPT",
    msg: replyMessage,
    time: dayjs().format('HH:mm'),
    type: 0,
  })
  loadding.value = false
}

const clearMessages = () => {
  messages.value = []
}

const refushCredit = async () => {
  loadding.value = true
  summary.value = await creditSummary()
  summary.value.total_available = summary.value.total_available.toFixed(2)
  console.log(summary.value)
  loadding.value = false
}
const updateApiKey = () => {
  visibleName.value = false
  //window.location.reload()
}

const noKey = () => {
  var ran = Math.floor(Math.random()*10);
  var timestamp = dayjs().format('mmss')
  var userNanme = "游客"+timestamp + "" + ran;
  user_id.value = userNanme;
  //visible.value = false
  //window.location.reload()
}

const updatePara = () => {
  visiblePara.value = false
}

onMounted(async () => {
  await refushCredit()
  console.log(user_id.value)
  if(user_id.value == "")
    visibleName.value = true

})
</script>

<template>
  <div id="layout">
    <header id="header" class="bg-dark-50 text-white h-10 select-none">
      <LoadingOutlined v-if="loadding" class="pl-3 cursor-pointer" />
      <span class="text-size-5 pl-5">chatGPT</span>
      <span class="pl-3">用户：{{ user_id }}</span>
      <a-tooltip>
        <template #title>清除聊天记录</template>
        <a-popconfirm title="确定清除本地所有聊天记录吗?" ok-text="是的" cancel-text="再想想" @confirm="clearMessages">
          <ClearOutlined class="pl-3 cursor-pointer" />
        </a-popconfirm>
      </a-tooltip>

      <a-tooltip>
        <template #title>设置用户名</template>
        <UserOutlined class="pl-3 cursor-pointer !text-red-400" @click="visibleName = true" />
      </a-tooltip>

      <a-tooltip>
        <template #title>设置参数</template>
        <SettingOutlined class="pl-3 cursor-pointer !text-red-400" @click="visiblePara = true" />
      </a-tooltip>

      <span class="float-right pr-3 pt-2">
        当前余额：{{ summary?.total_available }}
        <a-tooltip>
          <template #title>刷新余额</template>
          <RedoOutlined @click="refushCredit" />
        </a-tooltip>
      </span>
    </header>
    <div id="layout-body">
      <main id="main">
        <div class="flex-1 relative flex flex-col">
          <!-- header -->
          <!-- content -->
          <div class="flex-1 inset-0 overflow-hidden bg-transparent bg-bottom bg-cover flex flex-col">
            <!-- dialog -->
            <div class="flex-1 w-full self-center">
              <div class="relative px-3 py-1 m-auto flex flex-col">
                <div class="mx-0 my-1 self-center text-xs text-gray-400">
                  频道已创建
                </div>
                <div class="mx-0 my-1 self-center text-xs text-gray-400">
                  {{ createdAt }}
                </div>
                <Message :message=message v-for="message in messages" :class="message.type ? 'send' : 'replay'" />
              </div>
            </div>
          </div>
        </div>
      </main>
      <footer id="footer">
        <div class="relative p-4 w-full overflow-hidden text-gray-600 focus-within:text-gray-400 flex items-center">
          <a-textarea v-model:value="message" :auto-size="{ minRows: 2, maxRows: 5 }" placeholder="请输入消息..."
            class="appearance-none pl-10 py-2 w-full bg-white border border-gray-300 rounded-full text-sm placeholder-gray-800 focus:outline-none focus:border-blue-500 focus:border-blue-500 focus:shadow-outline-blue" />
          <span class="absolute inset-y-0 right-0 bottom-8 pr-6 flex items-end">
            <a-button shape="round" type="primary" @click="sendMessage">发送</a-button>
          </span>
        </div>

      </footer>
    </div>
    <a-modal v-model:visible="visibleName" title="请给自己输入一个名字吧" @ok="updateApiKey" @cancel="noKey" okText="确定" cancelText="取消">
      <a-alert message="起个好听的名字，让我记住你哦" type="info" />
      <div class="mt-2"></div>
      <a-input v-model:value="user_id" placeholder="请输入您的名字" />
    </a-modal>
    <a-modal v-model:visible="visiblePara" title="设置参数（慎重）"  @ok="updatePara" okText="确定" cancelText="关闭">
      <a-alert message="整数，不能超过1024" type="info" />
      <div class="mt-2"></div>
      <a-input-number v-model:value="max_tokens" :defaultValue="512" :max="512" :min="1"/>
      <div class="mt-2"></div>
      <a-alert message="0-2之间，数值越大随机性越高" type="info" />
      <div class="mt-2"></div>
      <a-input-number v-model:value="temperature" :defaultValue="1" :max="2" :min="0"/>
      <div class="mt-2"></div>
      <a-alert message="0-1之间，temperature的替代参数，一次只调整一个，不要两个一起修改" type="info" />
      <div class="mt-2"></div>
      <a-input-number v-model:value="top_p" :defaultValue="1" :max="1" :min="0"/>
    </a-modal>
  </div>
</template>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
}

#layout {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background-color: #f0f2f5;
}

#header {
  box-shadow: 2px 5px 5px 0px rgba(102, 102, 102, 0.5);
  flex-shrink: 0;
}

#layout-body {
  flex-grow: 2;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

#footer {
  height: 100px;
  flex-shrink: 0;
}

#main {
  flex-grow: 2;
}

.replay {
  float: left;
  clear: both;
}

.send {
  float: right;
  clear: both;
}
</style>
