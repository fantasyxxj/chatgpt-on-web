import { getRequest, postRequest } from "./api";
import { useStorage } from '@vueuse/core'
const user_id = useStorage('user_id', '')
const max_tokens = useStorage('max_tokens',512)
const temperature = useStorage('temperature',1)
const top_p = useStorage('top_p',1)

export const completion = async (text: string) => {
  const res = await postRequest({
    url: '/completions.do',
    data: {
      model: 'text-davinci-003',
      prompt: text,
      max_tokens: max_tokens.value,
      temperature: temperature.value,
      frequency_penalty: 0,
      presence_penalty: 0,
      top_p: top_p.value,
      user_id: user_id.value
    }
  })
  return res
}

export const creditSummary = async () => {
  return await getRequest({
    url: '/credit_summary.do'
  })
}
