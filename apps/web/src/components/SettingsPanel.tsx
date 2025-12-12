import { GenerateDialogueRequest } from '../api/client';

interface SettingsPanelProps {
  settings: Omit<GenerateDialogueRequest, 'dialogue_text'>;
  onChange: (settings: Omit<GenerateDialogueRequest, 'dialogue_text'>) => void;
  disabled?: boolean;
  onGenerate: () => void;
  onReset: () => void;
  isGenerating: boolean;
}

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'it', name: 'Italian' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'zh', name: 'Chinese' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' },
];

function SettingsPanel({
  settings,
  onChange,
  disabled = false,
  onGenerate,
  onReset,
  isGenerating,
}: SettingsPanelProps) {
  const updateSetting = <K extends keyof typeof settings>(
    key: K,
    value: (typeof settings)[K]
  ) => {
    onChange({ ...settings, [key]: value });
  };

  return (
    <div className="bg-dark-surface rounded-lg border border-dark-border p-6 space-y-6">
      <h2 className="text-xl font-semibold">Settings</h2>

      {/* Output Settings */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-dark-muted uppercase tracking-wide">
          Output Settings
        </h3>

        <div>
          <label className="block text-sm font-medium mb-2">
            Output Prefix
          </label>
          <input
            type="text"
            value={settings.output_prefix}
            onChange={(e) => updateSetting('output_prefix', e.target.value)}
            disabled={disabled}
            className="w-full bg-dark-bg text-dark-text border border-dark-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
            placeholder="conversation"
          />
        </div>
      </div>

      {/* TTS Parameters */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-dark-muted uppercase tracking-wide">
          TTS Parameters
        </h3>

        <div>
          <label className="block text-sm font-medium mb-2">
            Silence Between Lines: {settings.silence_ms}ms
          </label>
          <input
            type="range"
            min="0"
            max="2000"
            step="50"
            value={settings.silence_ms}
            onChange={(e) => updateSetting('silence_ms', parseInt(e.target.value))}
            disabled={disabled}
            className="w-full accent-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <div className="flex justify-between text-xs text-dark-muted mt-1">
            <span>0ms</span>
            <span>2000ms</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Language</label>
          <select
            value={settings.language}
            onChange={(e) => updateSetting('language', e.target.value)}
            disabled={disabled}
            className="w-full bg-dark-bg text-dark-text border border-dark-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Exaggeration: {settings.exaggeration.toFixed(1)}
          </label>
          <input
            type="range"
            min="1.0"
            max="3.0"
            step="0.1"
            value={settings.exaggeration}
            onChange={(e) => updateSetting('exaggeration', parseFloat(e.target.value))}
            disabled={disabled}
            className="w-full accent-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <div className="flex justify-between text-xs text-dark-muted mt-1">
            <span>1.0 (subtle)</span>
            <span>3.0 (dramatic)</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            CFG Weight: {settings.cfg_weight.toFixed(2)}
          </label>
          <input
            type="range"
            min="0.0"
            max="1.0"
            step="0.05"
            value={settings.cfg_weight}
            onChange={(e) => updateSetting('cfg_weight', parseFloat(e.target.value))}
            disabled={disabled}
            className="w-full accent-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <div className="flex justify-between text-xs text-dark-muted mt-1">
            <span>0.0</span>
            <span>1.0</span>
          </div>
        </div>
      </div>

      {/* Processing Options */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-dark-muted uppercase tracking-wide">
          Processing Options
        </h3>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={settings.process_audio}
            onChange={(e) => updateSetting('process_audio', e.target.checked)}
            disabled={disabled}
            className="w-4 h-4 rounded border-dark-border bg-dark-bg text-blue-500 focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <span className="text-sm">
            Enable audio processing
            <span className="block text-xs text-dark-muted">
              De-essing, normalization, fades
            </span>
          </span>
        </label>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={settings.save_individual}
            onChange={(e) => updateSetting('save_individual', e.target.checked)}
            disabled={disabled}
            className="w-4 h-4 rounded border-dark-border bg-dark-bg text-blue-500 focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <span className="text-sm">Save individual line files</span>
        </label>
      </div>

      {/* Device Selection */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-dark-muted uppercase tracking-wide">
          Device
        </h3>

        <div>
          <select
            value={settings.device}
            onChange={(e) => updateSetting('device', e.target.value)}
            disabled={disabled}
            className="w-full bg-dark-bg text-dark-text border border-dark-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <option value="cpu">CPU</option>
            <option value="cuda">CUDA (GPU)</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="pt-4 space-y-3">
        <button
          onClick={onGenerate}
          disabled={disabled || isGenerating}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-600/50 text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isGenerating ? (
            <>
              <svg
                className="animate-spin h-5 w-5"
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
              Generating...
            </>
          ) : (
            'Generate Conversation'
          )}
        </button>

        <button
          onClick={onReset}
          disabled={disabled || isGenerating}
          className="w-full bg-dark-bg hover:bg-dark-border border border-dark-border text-dark-text font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Reset Form
        </button>
      </div>
    </div>
  );
}

export default SettingsPanel;
