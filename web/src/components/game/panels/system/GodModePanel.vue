<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage, NInput, NSelect, NButton, NTextarea, NSlider, NTabs, NTabPane, NCard, NSpace, NScrollbar } from 'naive-ui'
import { godApi, avatarApi, type SimpleAvatarDTO } from '../../../../api'

const message = useMessage()
const loading = ref(false)
const avatarList = ref<SimpleAvatarDTO[]>([])

// === AI功能 ===
const aiPrompt = ref('')
const aiContext = ref('')
const aiResult = ref('')
const useFastModel = ref(true)

const selectedAvatarForSuggest = ref<string>('')
const aiSuggestion = ref('')

const selectedAvatarsForStory = ref<string[]>([])
const storyEventType = ref('奇遇')
const generatedStory = ref('')

// === 干预功能 ===
const selectedAvatarForFortune = ref<string>('')
const fortuneType = ref<'exp' | 'magic_stone' | 'hp'>('exp')
const fortuneValue = ref(1000)

const selectedAvatarForTribulation = ref<string>('')
const tribulationDifficulty = ref(5)

const eventText = ref('')
const eventAvatarIds = ref<string[]>([])
const eventIsMajor = ref(true)

// === 世界事件 ===
const competitionLocation = ref('天下第一擂台')
const treasureName = ref('')
const treasureLocation = ref('')
const disasterType = ref('earthquake')
const disasterLocation = ref('')
const disasterSeverity = ref(5)
const beastTideLocation = ref('')
const beastTideIntensity = ref(5)
const apocalypseType = ref('demon_invasion')

// === 特殊功能 ===
const possessorId = ref<string>('')
const possessionTargetId = ref<string>('')
const rebirthAvatarId = ref<string>('')
const rebirthType = ref('reincarnation')
const divinationAvatarId = ref<string>('')
const divinationQuestion = ref('')
const divinationResult = ref('')
const secretName = ref('')
const secretDesc = ref('')

// === 历史记录 ===
const godHistory = ref<any[]>([])

// === Computed ===
const avatarOptions = computed(() => {
  return avatarList.value.map(av => ({
    label: `${av.name} (${av.realm})`,
    value: av.id
  }))
})

const fortuneTypeOptions = [
  { label: '经验值 (EXP)', value: 'exp' },
  { label: '灵石 (Magic Stone)', value: 'magic_stone' },
  { label: '生命值 (HP)', value: 'hp' }
]

const storyEventTypeOptions = [
  { label: '奇遇', value: '奇遇' },
  { label: '战斗', value: '战斗' },
  { label: '情缘', value: '情缘' },
  { label: '突破', value: '突破' },
  { label: '探险', value: '探险' }
]

const disasterTypeOptions = [
  { label: '地震', value: 'earthquake' },
  { label: '洪水', value: 'flood' },
  { label: '旱灾', value: 'drought' },
  { label: '风暴', value: 'storm' }
]

const apocalypseTypeOptions = [
  { label: '魔族入侵', value: 'demon_invasion' },
  { label: '世界崩塌', value: 'world_collapse' },
  { label: '上古邪神复苏', value: 'ancient_evil' },
  { label: '虚空裂缝', value: 'void_tear' }
]

const rebirthTypeOptions = [
  { label: '轮回', value: 'reincarnation' },
  { label: '涅槃', value: 'nirvana' },
  { label: '重生', value: 'rebirth' }
]

// === Methods ===
async function loadAvatars() {
  try {
    const res = await avatarApi.fetchAvatarList()
    avatarList.value = res.avatars || []
  } catch (err) {
    console.error('Failed to load avatars:', err)
  }
}

async function handleAIGenerate() {
  if (!aiPrompt.value.trim()) {
    message.warning('请输入提示词')
    return
  }
  
  loading.value = true
  try {
    const res = await godApi.aiGenerate({
      prompt: aiPrompt.value,
      context: aiContext.value || undefined,
      use_fast_model: useFastModel.value
    })
    aiResult.value = res.result
    message.success('AI生成成功')
  } catch (err: any) {
    message.error(`生成失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleAISuggestEvent() {
  if (!selectedAvatarForSuggest.value) {
    message.warning('请选择角色')
    return
  }
  
  loading.value = true
  try {
    const res = await godApi.aiSuggestEvent({
      avatar_id: selectedAvatarForSuggest.value
    })
    aiSuggestion.value = res.suggestion
    message.success('AI建议生成成功')
  } catch (err: any) {
    message.error(`生成失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleAIGenerateStory() {
  if (selectedAvatarsForStory.value.length === 0) {
    message.warning('请至少选择一个角色')
    return
  }
  
  loading.value = true
  try {
    const res = await godApi.aiGenerateStory({
      avatar_ids: selectedAvatarsForStory.value,
      event_type: storyEventType.value
    })
    generatedStory.value = res.story
    message.success('剧情生成成功')
  } catch (err: any) {
    message.error(`生成失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleGrantFortune() {
  if (!selectedAvatarForFortune.value) {
    message.warning('请选择角色')
    return
  }
  
  loading.value = true
  try {
    await godApi.grantFortune({
      avatar_id: selectedAvatarForFortune.value,
      fortune_type: fortuneType.value,
      value: fortuneValue.value
    })
    message.success('机缘已赐予')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleSendTribulation() {
  if (!selectedAvatarForTribulation.value) {
    message.warning('请选择角色')
    return
  }
  
  loading.value = true
  try {
    await godApi.sendTribulation({
      avatar_id: selectedAvatarForTribulation.value,
      difficulty: tribulationDifficulty.value
    })
    message.success('天劫已降下')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerEvent() {
  if (!eventText.value.trim()) {
    message.warning('请输入事件描述')
    return
  }
  
  loading.value = true
  try {
    await godApi.triggerEvent({
      event_text: eventText.value,
      related_avatar_ids: eventAvatarIds.value.length > 0 ? eventAvatarIds.value : undefined,
      is_major: eventIsMajor.value
    })
    message.success('事件已触发')
    eventText.value = ''
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function loadHistory() {
  try {
    const res = await godApi.getHistory(20)
    godHistory.value = res.history || []
  } catch (err) {
    console.error('Failed to load history:', err)
  }
}

// === 世界事件处理函数 ===
async function handleTriggerCompetition() {
  loading.value = true
  try {
    await godApi.triggerCompetition({
      location: competitionLocation.value
    })
    message.success('比武大会已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerTreasure() {
  if (!treasureName.value.trim() || !treasureLocation.value.trim()) {
    message.warning('请输入宝物名称和地点')
    return
  }
  
  loading.value = true
  try {
    await godApi.triggerTreasure({
      treasure_name: treasureName.value,
      location: treasureLocation.value,
      rarity: 'legendary'
    })
    message.success('宝物出世已触发')
    treasureName.value = ''
    treasureLocation.value = ''
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerDisaster() {
  if (!disasterLocation.value.trim()) {
    message.warning('请输入灾害地点')
    return
  }
  
  loading.value = true
  try {
    await godApi.triggerDisaster({
      disaster_type: disasterType.value,
      location: disasterLocation.value,
      severity: disasterSeverity.value
    })
    message.success('自然灾害已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerBeastTide() {
  if (!beastTideLocation.value.trim()) {
    message.warning('请输入兽潮地点')
    return
  }
  
  loading.value = true
  try {
    await godApi.triggerBeastTide({
      location: beastTideLocation.value,
      intensity: beastTideIntensity.value
    })
    message.success('兽潮已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerApocalypse() {
  loading.value = true
  try {
    await godApi.triggerApocalypse({
      apocalypse_type: apocalypseType.value,
      severity: 10
    })
    message.success('灭世危机已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

// === 特殊功能处理函数 ===
async function handleTriggerPossession() {
  loading.value = true
  try {
    await godApi.triggerPossession({
      possessor_id: possessorId.value,
      target_id: possessionTargetId.value
    })
    message.success('夺舍已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleTriggerRebirth() {
  loading.value = true
  try {
    await godApi.triggerRebirth({
      avatar_id: rebirthAvatarId.value,
      rebirth_type: rebirthType.value
    })
    message.success('重生已触发')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handlePerformDivination() {
  loading.value = true
  try {
    const res = await godApi.performDivination({
      avatar_id: divinationAvatarId.value,
      question: divinationQuestion.value
    })
    divinationResult.value = res.result
    message.success('占卜完成')
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

async function handleSetWorldSecret() {
  loading.value = true
  try {
    await godApi.setWorldSecret({
      secret_name: secretName.value,
      secret_desc: secretDesc.value,
      reveal_condition: ''
    })
    message.success('世界秘密已设置')
    secretName.value = ''
    secretDesc.value = ''
    loadHistory()
  } catch (err: any) {
    message.error(`操作失败: ${err.message || err}`)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAvatars()
  loadHistory()
})
</script>

<template>
  <div class="god-mode-panel">
    <div class="panel-header">
      <h3>🌟 上帝模式 (God Mode)</h3>
      <p class="description">作为天道，掌控修仙世界的一切</p>
    </div>
    
    <NTabs type="line" animated>
      <!-- AI功能 -->
      <NTabPane name="ai" tab="🤖 AI助手">
        <NScrollbar style="max-height: 500px">
          <NSpace vertical size="large">
            <!-- AI文本生成 -->
            <NCard title="AI文本生成" size="small">
              <NSpace vertical>
                <NTextarea
                  v-model:value="aiPrompt"
                  placeholder="输入提示词，例如：生成一个关于修仙的故事..."
                  :rows="3"
                />
                <NTextarea
                  v-model:value="aiContext"
                  placeholder="可选：输入上下文信息"
                  :rows="2"
                />
                <div style="display: flex; align-items: center; gap: 10px;">
                  <NButton 
                    type="primary" 
                    @click="handleAIGenerate"
                    :loading="loading"
                  >
                    生成
                  </NButton>
                  <label style="display: flex; align-items: center; gap: 5px;">
                    <input type="checkbox" v-model="useFastModel" />
                    使用快速模型（免费）
                  </label>
                </div>
                <NTextarea
                  v-if="aiResult"
                  v-model:value="aiResult"
                  placeholder="生成结果..."
                  :rows="5"
                  readonly
                />
              </NSpace>
            </NCard>

            <!-- AI建议事件 -->
            <NCard title="AI建议角色事件" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="selectedAvatarForSuggest"
                  :options="avatarOptions"
                  placeholder="选择角色"
                  filterable
                />
                <NButton 
                  type="primary" 
                  @click="handleAISuggestEvent"
                  :loading="loading"
                  :disabled="!selectedAvatarForSuggest"
                >
                  获取AI建议
                </NButton>
                <NTextarea
                  v-if="aiSuggestion"
                  v-model:value="aiSuggestion"
                  placeholder="AI建议..."
                  :rows="3"
                  readonly
                />
              </NSpace>
            </NCard>

            <!-- AI生成剧情 -->
            <NCard title="AI生成剧情" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="selectedAvatarsForStory"
                  :options="avatarOptions"
                  placeholder="选择角色（可多选）"
                  multiple
                  filterable
                  :max-tag-count="3"
                />
                <NSelect
                  v-model:value="storyEventType"
                  :options="storyEventTypeOptions"
                  placeholder="选择事件类型"
                />
                <NButton 
                  type="primary" 
                  @click="handleAIGenerateStory"
                  :loading="loading"
                  :disabled="selectedAvatarsForStory.length === 0"
                >
                  生成剧情
                </NButton>
                <NTextarea
                  v-if="generatedStory"
                  v-model:value="generatedStory"
                  placeholder="生成的剧情..."
                  :rows="6"
                  readonly
                />
              </NSpace>
            </NCard>
          </NSpace>
        </NScrollbar>
      </NTabPane>

      <!-- 神力干预 -->
      <NTabPane name="intervention" tab="⚡ 神力干预">
        <NScrollbar style="max-height: 500px">
          <NSpace vertical size="large">
            <!-- 赐予机缘 -->
            <NCard title="赐予机缘" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="selectedAvatarForFortune"
                  :options="avatarOptions"
                  placeholder="选择角色"
                  filterable
                />
                <NSelect
                  v-model:value="fortuneType"
                  :options="fortuneTypeOptions"
                  placeholder="选择机缘类型"
                />
                <div>
                  <label>数值：{{ fortuneValue }}</label>
                  <NSlider 
                    v-model:value="fortuneValue" 
                    :min="100" 
                    :max="10000" 
                    :step="100"
                  />
                </div>
                <NButton 
                  type="success" 
                  @click="handleGrantFortune"
                  :loading="loading"
                  :disabled="!selectedAvatarForFortune"
                >
                  赐予
                </NButton>
              </NSpace>
            </NCard>

            <!-- 降下天劫 -->
            <NCard title="降下天劫" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="selectedAvatarForTribulation"
                  :options="avatarOptions"
                  placeholder="选择角色"
                  filterable
                />
                <div>
                  <label>难度等级：{{ tribulationDifficulty }}</label>
                  <NSlider 
                    v-model:value="tribulationDifficulty" 
                    :min="1" 
                    :max="10" 
                    :step="1"
                  />
                </div>
                <NButton 
                  type="error" 
                  @click="handleSendTribulation"
                  :loading="loading"
                  :disabled="!selectedAvatarForTribulation"
                >
                  降下天劫
                </NButton>
              </NSpace>
            </NCard>

            <!-- 触发事件 -->
            <NCard title="触发世界事件" size="small">
              <NSpace vertical>
                <NTextarea
                  v-model:value="eventText"
                  placeholder="输入事件描述..."
                  :rows="3"
                />
                <NSelect
                  v-model:value="eventAvatarIds"
                  :options="avatarOptions"
                  placeholder="相关角色（可选，可多选）"
                  multiple
                  filterable
                  :max-tag-count="3"
                />
                <label style="display: flex; align-items: center; gap: 5px;">
                  <input type="checkbox" v-model="eventIsMajor" />
                  重大事件
                </label>
                <NButton 
                  type="primary" 
                  @click="handleTriggerEvent"
                  :loading="loading"
                  :disabled="!eventText.trim()"
                >
                  触发事件
                </NButton>
              </NSpace>
            </NCard>
          </NSpace>
        </NScrollbar>
      </NTabPane>

      <!-- 世界事件 -->
      <NTabPane name="events" tab="🎭 世界事件">
        <NScrollbar style="max-height: 500px">
          <NSpace vertical size="large">
            <!-- 比武大会 -->
            <NCard title="触发比武大会" size="small">
              <NSpace vertical>
                <NInput
                  v-model:value="competitionLocation"
                  placeholder="比武大会地点，例如：天下第一擂台"
                />
                <NButton 
                  type="primary" 
                  @click="handleTriggerCompetition"
                  :loading="loading"
                >
                  触发比武大会
                </NButton>
              </NSpace>
            </NCard>

            <!-- 宝物出世 -->
            <NCard title="触发宝物出世" size="small">
              <NSpace vertical>
                <NInput
                  v-model:value="treasureName"
                  placeholder="宝物名称，例如：混沌至尊剑"
                />
                <NInput
                  v-model:value="treasureLocation"
                  placeholder="出现地点"
                />
                <NButton 
                  type="warning" 
                  @click="handleTriggerTreasure"
                  :loading="loading"
                >
                  触发宝物出世
                </NButton>
              </NSpace>
            </NCard>

            <!-- 自然灾害 -->
            <NCard title="触发自然灾害" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="disasterType"
                  :options="disasterTypeOptions"
                  placeholder="选择灾害类型"
                />
                <NInput
                  v-model:value="disasterLocation"
                  placeholder="灾害地点"
                />
                <div>
                  <label>严重程度：{{ disasterSeverity }}</label>
                  <NSlider 
                    v-model:value="disasterSeverity" 
                    :min="1" 
                    :max="10" 
                    :step="1"
                  />
                </div>
                <NButton 
                  type="error" 
                  @click="handleTriggerDisaster"
                  :loading="loading"
                >
                  触发自然灾害
                </NButton>
              </NSpace>
            </NCard>

            <!-- 兽潮 -->
            <NCard title="触发兽潮" size="small">
              <NSpace vertical>
                <NInput
                  v-model:value="beastTideLocation"
                  placeholder="兽潮地点"
                />
                <div>
                  <label>强度：{{ beastTideIntensity }}</label>
                  <NSlider 
                    v-model:value="beastTideIntensity" 
                    :min="1" 
                    :max="10" 
                    :step="1"
                  />
                </div>
                <NButton 
                  type="error" 
                  @click="handleTriggerBeastTide"
                  :loading="loading"
                >
                  触发兽潮
                </NButton>
              </NSpace>
            </NCard>

            <!-- 灭世危机 -->
            <NCard title="触发灭世危机" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="apocalypseType"
                  :options="apocalypseTypeOptions"
                  placeholder="选择危机类型"
                />
                <NButton 
                  type="error" 
                  @click="handleTriggerApocalypse"
                  :loading="loading"
                >
                  触发灭世危机
                </NButton>
              </NSpace>
            </NCard>
          </NSpace>
        </NScrollbar>
      </NTabPane>

      <!-- 特殊功能 -->
      <NTabPane name="special" tab="✨ 特殊功能">
        <NScrollbar style="max-height: 500px">
          <NSpace vertical size="large">
            <!-- 夺舍 -->
            <NCard title="触发夺舍" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="possessorId"
                  :options="avatarOptions"
                  placeholder="选择夺舍者"
                  filterable
                />
                <NSelect
                  v-model:value="possessionTargetId"
                  :options="avatarOptions"
                  placeholder="选择被夺舍者"
                  filterable
                />
                <NButton 
                  type="warning" 
                  @click="handleTriggerPossession"
                  :loading="loading"
                  :disabled="!possessorId || !possessionTargetId"
                >
                  触发夺舍
                </NButton>
              </NSpace>
            </NCard>

            <!-- 重生 -->
            <NCard title="触发重生" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="rebirthAvatarId"
                  :options="avatarOptions"
                  placeholder="选择角色"
                  filterable
                />
                <NSelect
                  v-model:value="rebirthType"
                  :options="rebirthTypeOptions"
                  placeholder="重生类型"
                />
                <NButton 
                  type="primary" 
                  @click="handleTriggerRebirth"
                  :loading="loading"
                  :disabled="!rebirthAvatarId"
                >
                  触发重生
                </NButton>
              </NSpace>
            </NCard>

            <!-- 占卜 -->
            <NCard title="执行占卜" size="small">
              <NSpace vertical>
                <NSelect
                  v-model:value="divinationAvatarId"
                  :options="avatarOptions"
                  placeholder="选择角色"
                  filterable
                />
                <NTextarea
                  v-model:value="divinationQuestion"
                  placeholder="输入占卜问题..."
                  :rows="2"
                />
                <NButton 
                  type="primary" 
                  @click="handlePerformDivination"
                  :loading="loading"
                  :disabled="!divinationAvatarId || !divinationQuestion"
                >
                  执行占卜
                </NButton>
                <NTextarea
                  v-if="divinationResult"
                  v-model:value="divinationResult"
                  placeholder="占卜结果..."
                  :rows="3"
                  readonly
                />
              </NSpace>
            </NCard>

            <!-- 世界秘密 -->
            <NCard title="设置世界秘密" size="small">
              <NSpace vertical>
                <NInput
                  v-model:value="secretName"
                  placeholder="秘密名称"
                />
                <NTextarea
                  v-model:value="secretDesc"
                  placeholder="秘密描述..."
                  :rows="3"
                />
                <NButton 
                  type="primary" 
                  @click="handleSetWorldSecret"
                  :loading="loading"
                  :disabled="!secretName || !secretDesc"
                >
                  设置世界秘密
                </NButton>
              </NSpace>
            </NCard>
          </NSpace>
        </NScrollbar>
      </NTabPane>

      <!-- 行为历史 -->
      <NTabPane name="history" tab="📜 历史记录">
        <NScrollbar style="max-height: 500px">
          <div class="history-list">
            <div v-if="godHistory.length === 0" class="empty-history">
              暂无记录
            </div>
            <div 
              v-for="(action, idx) in godHistory" 
              :key="idx" 
              class="history-item"
              :class="{ 'ai-used': action.ai_used }"
            >
              <div class="history-time">{{ action.timestamp }}</div>
              <div class="history-ability">{{ action.ability }}</div>
              <div class="history-desc">{{ action.description }}</div>
              <div v-if="action.result" class="history-result">
                结果: {{ action.result }}
              </div>
              <div v-if="action.ai_used" class="ai-badge">🤖 AI</div>
            </div>
          </div>
          <NButton 
            type="primary" 
            size="small" 
            @click="loadHistory"
            style="margin-top: 10px;"
          >
            刷新
          </NButton>
        </NScrollbar>
      </NTabPane>
    </NTabs>
  </div>
</template>

<style scoped>
.god-mode-panel {
  padding: 20px;
}

.panel-header {
  margin-bottom: 20px;
}

.panel-header h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #ffd700;
}

.panel-header .description {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty-history {
  text-align: center;
  color: #999;
  padding: 20px;
}

.history-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 4px;
  border-left: 3px solid #666;
  position: relative;
}

.history-item.ai-used {
  border-left-color: #00bcd4;
}

.history-time {
  font-size: 11px;
  color: #888;
}

.history-ability {
  font-size: 12px;
  color: #ffd700;
  font-weight: bold;
  margin-top: 3px;
}

.history-desc {
  font-size: 13px;
  margin-top: 5px;
}

.history-result {
  font-size: 12px;
  color: #4caf50;
  margin-top: 5px;
}

.ai-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  font-size: 11px;
}
</style>
