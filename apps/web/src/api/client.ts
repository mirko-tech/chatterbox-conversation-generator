/**
 * API Client for Chatterbox Dialogue Generator
 *
 * Handles communication with the FastAPI backend.
 */

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Type definitions matching the backend models
export interface GenerateDialogueRequest {
  dialogue_text: string;
  output_prefix: string;
  silence_ms: number;
  language: string;
  exaggeration: number;
  cfg_weight: number;
  save_individual: boolean;
  process_audio: boolean;
  device: string;
}

export interface GenerateDialogueResponse {
  status: string;
  output_file: string;
  lines_dir: string | null;
  duration_seconds: number;
  num_lines: number;
  timestamp: string;
}

export interface ErrorResponse {
  status: string;
  error: string;
  details?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

// API Client class
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Check if the API is healthy
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate a dialogue audio file
   */
  async generateDialogue(
    request: GenerateDialogueRequest
  ): Promise<GenerateDialogueResponse> {
    const response = await fetch(`${this.baseUrl}/api/generate-dialogue`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();

    if (!response.ok) {
      // Backend returns error in detail field
      const errorData = data.detail || data;
      throw new Error(errorData.details || errorData.error || 'Generation failed');
    }

    return data;
  }

  /**
   * Get download URL for a generated file
   */
  getDownloadUrl(filePath: string): string {
    return `${this.baseUrl}/api/download?path=${encodeURIComponent(filePath)}`;
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();
