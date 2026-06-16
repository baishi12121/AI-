import { defineStore } from 'pinia'
import { ref } from 'vue'
import { get, set, del } from 'idb-keyval'
import type { AnalysisResult } from '@/api/client'

const KEY = 'aichatcoach:history'
const MAX = 20

export interface HistoryItem {
  id: string
  created_at: number
  input_type: 'text' | 'image'
  preview: string
  result: AnalysisResult
}

export const useHistoryStore = defineStore('history', () => {
  const items = ref<HistoryItem[]>([])

  async function load() {
    const data = (await get(KEY)) as HistoryItem[] | undefined
    items.value = Array.isArray(data) ? data : []
  }

  async function add(item: HistoryItem) {
    const next = [item, ...items.value.filter((i) => i.id !== item.id)].slice(0, MAX)
    items.value = next
    await set(KEY, next)
  }

  async function remove(id: string) {
    items.value = items.value.filter((i) => i.id !== id)
    await set(KEY, items.value)
  }

  async function clear() {
    items.value = []
    await del(KEY)
  }

  function findById(id: string): HistoryItem | undefined {
    return items.value.find((i) => i.id === id)
  }

  return { items, load, add, remove, clear, findById }
})
