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
  }
};
