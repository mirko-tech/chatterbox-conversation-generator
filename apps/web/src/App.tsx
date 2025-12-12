import { useState, useEffect, useRef } from 'react';
import { apiClient, GenerateDialogueRequest, GenerateDialogueResponse } from './api/client';
import DialogueEditor from './components/DialogueEditor';
import SettingsPanel from './components/SettingsPanel';
import StatusDisplay from './components/StatusDisplay';

interface ProgressData {
  current_line: number;
  total_lines: number;
  status: 'idle' | 'generating_line' | 'merging' | 'completed' | 'error';
  message: string;
}

// Default settings
const DEFAULT_SETTINGS: Omit<GenerateDialogueRequest, 'dialogue_text'> = {
  output_prefix: 'conversation',
  silence_ms: 500,
  language: 'en',
  exaggeration: 1.5,
  cfg_weight: 0.5,
  save_individual: true,
  process_audio: true,
  device: 'cpu',
};

function App() {
  // State
  const [dialogueText, setDialogueText] = useState('');
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<GenerateDialogueResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  // Setup progress streaming
  useEffect(() => {
    if (isGenerating) {
      // Start listening to progress updates
      const eventSource = new EventSource('http://localhost:8000/api/progress-stream');
      eventSourceRef.current = eventSource;

      eventSource.onmessage = (event) => {
        const data: ProgressData = JSON.parse(event.data);
        setProgress(data);
      };

      eventSource.onerror = () => {
        eventSource.close();
      };

      return () => {
        eventSource.close();
      };
    }
  }, [isGenerating]);

  // Handle generation
  const handleGenerate = async () => {
    if (!dialogueText.trim()) {
      setError('Please enter dialogue text');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setResult(null);
    setProgress(null);

    try {
      const response = await apiClient.generateDialogue({
        dialogue_text: dialogueText,
        ...settings,
      });

      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsGenerating(false);
      // Close event source when done
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    }
  };

  // Handle reset
  const handleReset = () => {
    setDialogueText('');
    setSettings(DEFAULT_SETTINGS);
    setError(null);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-dark-bg text-dark-text">
      {/* Header */}
      <header className="border-b border-dark-border bg-dark-surface/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold">Chatterbox Dialogue Generator</h1>
            <p className="text-dark-muted">
              Generate multi-speaker AI conversations with voice cloning and natural audio processing
            </p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs bg-blue-500/10 text-blue-400 px-2 py-1 rounded border border-blue-500/20">
                Powered by Chatterbox TTS
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Dialogue Editor (2/3 width) */}
          <div className="lg:col-span-2">
            <DialogueEditor
              value={dialogueText}
              onChange={setDialogueText}
              disabled={isGenerating}
            />
          </div>

          {/* Right Column - Settings Panel (1/3 width) */}
          <div className="lg:col-span-1">
            <SettingsPanel
              settings={settings}
              onChange={setSettings}
              disabled={isGenerating}
              onGenerate={handleGenerate}
              onReset={handleReset}
              isGenerating={isGenerating}
            />
          </div>
        </div>

        {/* Status Display */}
        <div className="mt-8">
          <StatusDisplay
            isGenerating={isGenerating}
            result={result}
            error={error}
            progress={progress}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-border mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-dark-muted text-sm">
            Built with ❤️ by Mirko Guarnaccia for the open source community
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
