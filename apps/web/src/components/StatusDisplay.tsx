import { GenerateDialogueResponse } from '../api/client';
import { apiClient } from '../api/client';

interface ProgressData {
  current_line: number;
  total_lines: number;
  status: 'idle' | 'generating_line' | 'merging' | 'completed' | 'error';
  message: string;
}

interface StatusDisplayProps {
  isGenerating: boolean;
  result: GenerateDialogueResponse | null;
  error: string | null;
  progress: ProgressData | null;
}

function StatusDisplay({ isGenerating, result, error, progress }: StatusDisplayProps) {
  if (!isGenerating && !result && !error) {
    return (
      <div className="bg-dark-surface rounded-lg border border-dark-border p-6">
        <div className="flex items-center gap-3 text-dark-muted">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p>Ready to generate. Enter your dialogue and click "Generate Conversation".</p>
        </div>
      </div>
    );
  }

  if (isGenerating) {
    const progressPercentage = progress?.total_lines
      ? Math.round((progress.current_line / progress.total_lines) * 100)
      : 0;

    return (
      <div className="bg-dark-surface rounded-lg border border-blue-500/30 p-6">
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-blue-400">
            <svg
              className="animate-spin h-6 w-6 flex-shrink-0"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <div className="flex-1">
              <p className="font-medium">Generating conversation...</p>
              {progress?.message && (
                <p className="text-sm text-dark-muted mt-1">
                  {progress.message}
                </p>
              )}
            </div>
          </div>

          {/* Progress Bar */}
          {progress && progress.total_lines > 0 && (
            <div className="space-y-2">
              <div className="w-full bg-dark-border rounded-full h-2 overflow-hidden">
                <div
                  className="bg-blue-500 h-full transition-all duration-300 ease-out"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-dark-muted">
                <span>
                  {progress.current_line} of {progress.total_lines} lines
                </span>
                <span>{progressPercentage}%</span>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 rounded-lg border border-red-500/30 p-6">
        <div className="flex items-start gap-3 text-red-400">
          <svg
            className="w-6 h-6 flex-shrink-0 mt-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div className="flex-1">
            <p className="font-medium">Generation Failed</p>
            <p className="text-sm mt-1 text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (result) {
    const downloadUrl = apiClient.getDownloadUrl(result.output_file);

    return (
      <div className="bg-green-500/10 rounded-lg border border-green-500/30 p-6">
        <div className="flex items-start gap-3">
          <svg
            className="w-6 h-6 flex-shrink-0 mt-0.5 text-green-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div className="flex-1">
            <p className="font-medium text-green-400 mb-3">
              Conversation Generated Successfully!
            </p>

            <div className="space-y-2 text-sm text-dark-text">
              <div className="flex items-center justify-between">
                <span className="text-dark-muted">Output File:</span>
                <span className="font-mono text-xs">{result.output_file}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-dark-muted">Duration:</span>
                <span>{result.duration_seconds.toFixed(2)} seconds</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-dark-muted">Lines Generated:</span>
                <span>{result.num_lines}</span>
              </div>

              {result.lines_dir && (
                <div className="flex items-center justify-between">
                  <span className="text-dark-muted">Individual Lines:</span>
                  <span className="font-mono text-xs">{result.lines_dir}</span>
                </div>
              )}
            </div>

            <div className="mt-4 flex gap-3">
              <a
                href={downloadUrl}
                download
                className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
                Download WAV
              </a>

              {result.lines_dir && (
                <button
                  onClick={() => alert(`Individual lines saved to:\n${result.lines_dir}`)}
                  className="inline-flex items-center gap-2 bg-dark-bg hover:bg-dark-border border border-dark-border text-dark-text font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                    />
                  </svg>
                  View Line Files
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

export default StatusDisplay;
