const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private _token: string | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this._token = localStorage.getItem('token');
    }
  }

  get token(): string | null {
    return this._token;
  }

  get isAuthenticated(): boolean {
    return this._token !== null;
  }

  setToken(token: string) {
    this._token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  clearToken() {
    this._token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const mergedHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      mergedHeaders['Authorization'] = `Bearer ${this.token}`;
    }

    const headers = new Headers(mergedHeaders);
    if (headers.get('Content-Type') === '') {
      headers.delete('Content-Type');
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 204) {
      return {} as T;
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return data as T;
  }

  async login(email: string, password: string) {
    const data = await this.request<any>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.access_token);
    return data;
  }

  async register(name: string, email: string, password: string) {
    const data = await this.request<any>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
    this.setToken(data.access_token);
    return data;
  }

  async getMe() {
    return this.request<any>('/auth/me');
  }

  async getCurrentLevel() {
    return this.request<any>('/levels/current');
  }

  async getLevelProgress() {
    return this.request<any>('/levels/');
  }

  async getLevel(levelNumber: number) {
    return this.request<any>(`/levels/${levelNumber}`);
  }

  async getQuiz(levelNumber: number) {
    return this.request<any>(`/levels/${levelNumber}/quiz`);
  }

  async submitQuiz(levelNumber: number, answers: number[]) {
    return this.request<any>(`/levels/${levelNumber}/quiz/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers }),
    });
  }

  async startInterview(levelNumber: number) {
    return this.request<any>('/interview/start', {
      method: 'POST',
      body: JSON.stringify({ level_number: levelNumber }),
    });
  }

  async submitInterview(attemptId: number, answers: number[]) {
    return this.request<any>('/interview/submit', {
      method: 'POST',
      body: JSON.stringify({ attempt_id: attemptId, answers }),
    });
  }

  async getInterviewHistory() {
    return this.request<any>('/interview/history');
  }

  async getInterviewPrompt(levelNumber: number) {
    return this.request<any>(`/interview/prompt/${levelNumber}`);
  }

  async getLeaderboard(limit = 20) {
    return this.request<any>(`/leaderboard?limit=${limit}`);
  }

  async submitNotes(levelNumber: number, files: File[]) {
    const formData = new FormData();
    formData.append('level_number', levelNumber.toString());
    files.forEach(f => formData.append('files', f));
    return this.request<any>('/notes/submit', {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': '' }, // Let fetch set multipart boundary
    });
  }

  async getNotesStatus(levelNumber: number) {
    return this.request<any>(`/notes/status/${levelNumber}`);
  }

  async getAchievements() {
    return this.request<any>('/achievements/');
  }
}

export const api = new ApiClient();
