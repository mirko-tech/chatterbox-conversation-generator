import { useState } from 'react';

interface DialogueEditorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const EXAMPLE_DIALOGUE = `voice1_wav="voices/agent.flac"
voice2_wav="voices/customer.flac"

voice1="Hello! Thank you for calling our support center. How can I help you today?"
voice2="Hi, I'm having trouble logging into my account. It keeps saying my password is incorrect."
voice1="I'm sorry to hear that. Let me help you reset your password. Can you provide your email address?"
voice2="Sure, it's john.doe@example.com"
voice1="Thank you. I've sent a password reset link to that email. Please check your inbox."
voice2="Got it! I see the email. Thank you so much for your help!"
voice1="You're welcome! Is there anything else I can assist you with today?"
voice2="No, that's all. Have a great day!"
voice1="You too! Goodbye!"`;

function DialogueEditor({ value, onChange, disabled = false }: DialogueEditorProps) {
  const [showHelp, setShowHelp] = useState(false);

  const handleLoadExample = () => {
    onChange(EXAMPLE_DIALOGUE);
  };

  return (
    <div className="bg-dark-surface rounded-lg border border-dark-border p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Dialogue Editor</h2>
        <button
          onClick={handleLoadExample}
          disabled={disabled}
          className="text-sm text-blue-400 hover:text-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Load Example
        </button>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder={`Enter your dialogue here...\n\nExample:\nvoice1_wav="voices/speaker1.wav"\nvoice2_wav="voices/speaker2.wav"\n\nvoice1="Hello, how are you?"\nvoice2="I'm doing great, thanks!"`}
        className="w-full h-96 bg-dark-bg text-dark-text border border-dark-border rounded-lg p-4 font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
        spellCheck={false}
      />

      <div className="mt-4 space-y-2">
        <button
          onClick={() => setShowHelp(!showHelp)}
          className="text-sm text-dark-muted hover:text-dark-text flex items-center gap-2"
        >
          <svg
            className={`w-4 h-4 transition-transform ${showHelp ? 'rotate-90' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
          Format Guide
        </button>

        {showHelp && (
          <div className="bg-dark-bg rounded-lg p-4 text-sm space-y-2 border border-dark-border">
            <p className="text-dark-muted">
              Define voice templates at the top, then write dialogue lines:
            </p>
            <pre className="text-dark-text bg-dark-surface p-3 rounded border border-dark-border overflow-x-auto">
{`voice1_wav="voices/speaker1.wav"
voice2_wav="voices/speaker2.wav"

voice1="Hello, how are you?"
voice2="I'm doing great!"`}
            </pre>
            <ul className="text-dark-muted list-disc list-inside space-y-1">
              <li>Voice files can be WAV or FLAC format</li>
              <li>Reference files in the <code className="text-blue-400">voices/</code> folder</li>
              <li>Even short voice samples (5-10 seconds) work well</li>
              <li>Each line should be at least 3 characters long</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default DialogueEditor;
