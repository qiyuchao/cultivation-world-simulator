import { httpClient } from '../http';

export interface GodAIGenerateParams {
  prompt: string;
  context?: string;
  use_fast_model?: boolean;
}

export interface GodModifyAttributeParams {
  avatar_id: string;
  attribute: string;
  value: any;
}

export interface GodFortuneParams {
  avatar_id: string;
  fortune_type: 'exp' | 'magic_stone' | 'hp';
  value: number;
}

export interface GodTribulationParams {
  avatar_id: string;
  difficulty: number;
}

export interface GodEventParams {
  event_text: string;
  related_avatar_ids?: string[];
  is_major?: boolean;
}

export interface GodAISuggestParams {
  avatar_id: string;
}

export interface GodAIStoryParams {
  avatar_ids: string[];
  event_type?: string;
}

export interface GodQiParams {
  tile_id: string;
  delta: number;
}

export interface GodActionHistory {
  ability: string;
  description: string;
  timestamp: string;
  target_ids: string[];
  result?: string;
  ai_used: boolean;
}

export const godApi = {
  /**
   * AI生成文本
   */
  aiGenerate(params: GodAIGenerateParams) {
    return httpClient.post<{ status: string; result: string }>('/api/god/ai_generate', params);
  },

  /**
   * AI建议角色事件
   */
  aiSuggestEvent(params: GodAISuggestParams) {
    return httpClient.post<{ status: string; suggestion: string }>('/api/god/ai_suggest_event', params);
  },

  /**
   * AI生成剧情
   */
  aiGenerateStory(params: GodAIStoryParams) {
    return httpClient.post<{ status: string; story: string }>('/api/god/ai_generate_story', params);
  },

  /**
   * 修改角色属性
   */
  modifyAttribute(params: GodModifyAttributeParams) {
    return httpClient.post<{ status: string; message: string }>('/api/god/modify_attribute', params);
  },

  /**
   * 赐予机缘
   */
  grantFortune(params: GodFortuneParams) {
    return httpClient.post<{ status: string; message: string }>('/api/god/grant_fortune', params);
  },

  /**
   * 降下天劫
   */
  sendTribulation(params: GodTribulationParams) {
    return httpClient.post<{ status: string; message: string }>('/api/god/send_tribulation', params);
  },

  /**
   * 触发世界事件
   */
  triggerEvent(params: GodEventParams) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_event', params);
  },

  /**
   * 调整地块灵气
   */
  adjustQi(params: GodQiParams) {
    return httpClient.post<{ status: string; message: string }>('/api/god/adjust_qi', params);
  },

  /**
   * 获取上帝行为历史
   */
  getHistory(limit?: number) {
    return httpClient.get<{ status: string; history: GodActionHistory[] }>(
      `/api/god/history${limit ? `?limit=${limit}` : ''}`
    );
  },

  /**
   * 触发比武大会
   */
  triggerCompetition(params: { location: string; participants?: string[] }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_competition', params);
  },

  /**
   * 触发宝物出世
   */
  triggerTreasure(params: { treasure_name: string; location: string; rarity?: string }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_treasure', params);
  },

  /**
   * 触发自然灾害
   */
  triggerDisaster(params: { disaster_type: string; location: string; severity?: number }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_disaster', params);
  },

  /**
   * 触发兽潮
   */
  triggerBeastTide(params: { location: string; intensity?: number }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_beast_tide', params);
  },

  /**
   * 触发夺舍
   */
  triggerPossession(params: { possessor_id: string; target_id: string }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_possession', params);
  },

  /**
   * 触发重生
   */
  triggerRebirth(params: { avatar_id: string; rebirth_type?: string }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_rebirth', params);
  },

  /**
   * 执行占卜
   */
  performDivination(params: { avatar_id: string; question: string }) {
    return httpClient.post<{ status: string; result: string }>('/api/god/perform_divination', params);
  },

  /**
   * 设置世界秘密
   */
  setWorldSecret(params: { secret_name: string; secret_desc: string; reveal_condition?: string }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/set_world_secret', params);
  },

  /**
   * 触发灭世危机
   */
  triggerApocalypse(params: { apocalypse_type: string; severity?: number }) {
    return httpClient.post<{ status: string; message: string }>('/api/god/trigger_apocalypse', params);
  }
};
