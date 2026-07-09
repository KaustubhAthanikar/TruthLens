import React, { useState, useEffect, useRef } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  AlertCircle,
  Upload,
  Globe,
  Cpu,
  Layers,
  Search,
  ArrowLeft,
  FileText,
  Sparkles,
  ExternalLink,
  HelpCircle
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL;

function App() {
  const [tab, setTab] = useState('text'); // 'text' | 'image'
  const [claimText, setClaimText] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [selectedClaimIndex, setSelectedClaimIndex] = useState(0);
  const [error, setError] = useState(null);
  const [extractedOcrText, setExtractedOcrText] = useState('');
  const [processedOcrText, setProcessedOcrText] = useState('');

  const fileInputRef = useRef(null);

  // Scan Steps for the loading animation tracker
  const scanSteps = [
    { label: 'Analyzing statement syntax & extracting claims', icon: <Layers size={16} /> },
    { label: 'Formulating search query & checking local cache', icon: <Search size={16} /> },
    { label: 'Retrieving evidence documents from search indexing', icon: <Globe size={16} /> },
    { label: 'Analyzing sources and ranking factual relevance', icon: <Cpu size={16} /> },
    { label: 'Synthesizing report verdict with deep reasoning engine', icon: <Sparkles size={16} /> }
  ];

  // Dynamic step simulation during loading
  useEffect(() => {
    let interval = null;
    if (loading) {
      setCurrentStep(0);
      interval = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev < scanSteps.length - 1) {
            return prev + 1;
          }
          return prev;
        });
      }, 2500);
    } else {
      setCurrentStep(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [loading]);

  // Drag and Drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        handleImageSelection(file);
      } else {
        setError('Please drop a valid image file (PNG, JPG, WEBP).');
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleImageSelection(e.target.files[0]);
    }
  };

  const handleImageSelection = (file) => {
    setImageFile(file);
    if (file.size > 5 * 1024 * 1024) {

      setError(
        "Image must be below 5MB"
      );

      return;
    }
    setError(null);
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleRemoveImage = (e) => {
    e.stopPropagation();
    setImageFile(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Submission handler
  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
    setSelectedClaimIndex(0);
    setExtractedOcrText('');
    setProcessedOcrText('');

    try {
      if (tab === 'text') {
        if (!claimText.trim()) {
          throw new Error('Please enter a claim statement to verify.');
        }

        const response = await fetch(`${API_BASE_URL}/api/claims/verify`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: claimText })
        });

        if (!response.ok) {
          throw new Error(`Server returned status code: ${response.status}`);
        }

        const data = await response.json();
        setResult(data.data);
      } else {
        if (!imageFile) {
          throw new Error('Please select or upload an image file.');
        }

        const formData = new FormData();
        formData.append('image', imageFile);

        const response = await fetch(`${API_BASE_URL}/api/images/verify`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`Server returned status code: ${response.status}`);
        }

        const data = await response.json();
        setExtractedOcrText(data.extracted_text);
        setProcessedOcrText(data.processed_text);
        setResult(data.result);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || 'An unexpected error occurred. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setClaimText('');
    setImageFile(null);
    setImagePreview(null);
    setExtractedOcrText('');
    setProcessedOcrText('');
    setSelectedClaimIndex(0);
  };

  // Compute values for UI rendering
  const activeClaim = result && result.claims && result.claims[selectedClaimIndex];

  const getVerdictTheme = (verdict) => {
    const v = String(verdict).toUpperCase();
    if (v === 'SUPPORTS' || v === 'MOSTLY TRUE') {
      return {
        class: 'bg-brand-true/5 border border-brand-true/20',
        textClass: 'text-brand-true',
        label: 'Mostly True',
        icon: <ShieldCheck size={32} className="text-brand-true" />,
        color: 'var(--color-brand-true)'
      };
    } else if (v === 'REFUTES' || v === 'LIKELY FALSE') {
      return {
        class: 'bg-brand-false/5 border border-brand-false/20',
        textClass: 'text-brand-false',
        label: 'Likely False',
        icon: <ShieldAlert size={32} className="text-brand-false" />,
        color: 'var(--color-brand-false)'
      };
    } else {
      return {
        class: 'bg-brand-warn/5 border border-brand-warn/20',
        textClass: 'text-brand-warn',
        label: 'Needs Context',
        icon: <AlertCircle size={32} className="text-brand-warn" />,
        color: 'var(--color-brand-warn)'
      };
    }
  };

  const activeVerdict = activeClaim ? getVerdictTheme(
    activeClaim.trust_report?.display_verdict
    ||
    activeClaim.verification.verdict) : null;

  // Circular progress math
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const confidenceScore = activeClaim ? (activeClaim.verification.confidence || 0) : 0;
  const confidencePercent = confidenceScore <= 1 ? Math.round(confidenceScore * 100) : Math.round(confidenceScore);
  const strokeDashoffset = circumference - (confidencePercent / 100) * circumference;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 md:py-12">
      <header className="flex justify-between items-center pb-5 mb-8 border-b border-brand-border">
        <div className="flex items-center gap-3 cursor-pointer select-none" onClick={handleReset}>
          <div className="w-9 h-9 flex items-center justify-center bg-brand-primary rounded-lg text-white">
            <ShieldCheck size={20} strokeWidth={2.5} />
          </div>
          <span className="font-sans text-xl font-bold tracking-tight text-white">
            TruthLens<span className="text-[10px] px-2 py-0.5 bg-brand-border border border-white/5 rounded-full text-slate-400 font-sans font-medium ml-2 align-middle">v1.0</span>
          </span>
        </div>
      </header>

      {error && (
        <div className="bg-brand-false/10 border border-brand-false/25 rounded-lg p-4 text-red-200 mb-6 flex items-center gap-3 text-sm">
          <AlertCircle size={18} className="flex-shrink-0 text-brand-false" />
          <div>
            <strong>Verification Failed:</strong> {error}
          </div>
        </div>
      )}

      {/* Main Grid */}
      <main className="grid grid-cols-1 gap-6">
        {!loading && !result ? (
          /* WORKSPACE INPUT PANEL */
          <div className="bg-brand-bg-surface border border-brand-border rounded-xl p-6 md:p-8 shadow-sm">
            <h1 className="font-sans text-xl md:text-2xl font-bold mb-1.5 text-white">Scan Claims & Verify Information</h1>
            <p className="text-slate-400 text-sm mb-6">Verify assertions, search web sources, extract OCR content, and run credibility intelligence.</p>

            <div className="flex gap-2 mb-5 overflow-x-auto pb-1">
              <button
                className={`px-3.5 py-2 rounded-lg border font-semibold text-xs md:text-sm cursor-pointer flex items-center gap-1.5 transition duration-200 select-none ${tab === 'text' ? 'bg-brand-primary/10 border-brand-primary text-white' : 'border-brand-border text-slate-400 hover:text-white hover:bg-white/[0.01]'}`}
                onClick={() => setTab('text')}
              >
                <FileText size={16} />
                Text Claim
              </button>
              <button
                className={`px-3.5 py-2 rounded-lg border font-semibold text-xs md:text-sm cursor-pointer flex items-center gap-1.5 transition duration-200 select-none ${tab === 'image' ? 'bg-brand-primary/10 border-brand-primary text-white' : 'border-brand-border text-slate-400 hover:text-white hover:bg-white/[0.01]'}`}
                onClick={() => setTab('image')}
              >
                <Upload size={16} />
                Social Media Image
              </button>
            </div>

            <form onSubmit={handleVerify}>
              {tab === 'text' ? (
                <div className="relative mb-5">
                  <textarea
                    className="w-full h-36 bg-black/20 border border-brand-border rounded-lg p-3 text-white font-sans text-sm md:text-base resize-none outline-none focus:border-brand-primary transition-all duration-200 placeholder-slate-600"
                    placeholder="Paste a claim, tweet statement, headline or WhatsApp forward here to analyze truthfulness..."
                    value={claimText}
                    onChange={(e) => setClaimText(e.target.value)}
                    maxLength={1000}
                  />
                  <div className="absolute bottom-2.5 right-3 text-[10px] text-slate-500">{claimText.length}/1000 chars</div>
                </div>
              ) : (
                <div
                  className={`border border-dashed rounded-lg py-10 px-6 text-center cursor-pointer bg-black/10 transition-all duration-200 flex flex-col items-center justify-center gap-3.5 mb-5 ${dragActive ? 'border-brand-secondary bg-black/20' : 'border-brand-border hover:border-brand-secondary'}`}
                  onDragEnter={handleDrag}
                  onDragOver={handleDrag}
                  onDragLeave={handleDrag}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current.click()}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleFileChange}
                  />

                  {!imagePreview ? (
                    <>
                      <div className="w-12 h-12 rounded-full border border-brand-border flex items-center justify-center text-slate-400 transition-all duration-200">
                        <Upload size={20} />
                      </div>
                      <div className="font-sans font-semibold text-white text-sm md:text-base">Drag & drop your screenshot or click to browse</div>
                      <div className="text-xs text-slate-500">Supports PNG, JPG, JPEG, WEBP up to 5MB</div>
                    </>
                  ) : (
                    <div className="relative w-full max-w-xs rounded-lg overflow-hidden border border-brand-border mt-1" onClick={(e) => e.stopPropagation()}>
                      <img src={imagePreview} alt="Screenshot Preview" className="w-full h-auto block" />
                      <button className="absolute top-1.5 right-1.5 bg-black/70 hover:bg-brand-false text-white rounded-full w-7 h-7 flex items-center justify-center cursor-pointer transition-all duration-200" onClick={handleRemoveImage} title="Remove image">
                        &times;
                      </button>
                    </div>
                  )}
                </div>
              )}

              <button
                type="submit"
                className="w-full bg-brand-primary hover:bg-brand-primary/95 text-white py-3 px-5 rounded-lg font-semibold text-sm md:text-base cursor-pointer flex items-center justify-center gap-2 transition duration-200 active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed select-none"
                disabled={tab === 'text' ? !claimText.trim() : !imageFile}
              >
                <Sparkles size={16} />
                Analyze and Fact-Check
              </button>
            </form>
          </div>
        ) : loading ? (
          /* SCANNING TRACKER PANEL */
          <div className="bg-brand-bg-surface border border-brand-border rounded-xl p-6 md:p-8 shadow-sm">
            <div className="flex flex-col items-center py-8 px-2">
              <div className="relative w-20 h-20 mb-8">
                <div className="w-full h-full border-2 border-brand-primary/10 border-t-brand-primary border-r-brand-secondary rounded-full animate-spin-slow"></div>
                <div className="absolute top-[12.5%] left-[12.5%] w-[75%] h-[75%] bg-brand-bg-surface border border-brand-border rounded-full flex items-center justify-center">
                  <Search size={24} className="text-brand-warn animate-pulse-glow" />
                </div>
              </div>

              <h2 className="font-sans text-xl font-bold mb-1.5 text-center text-white">Verifying Source Credibility</h2>
              <p className="text-slate-400 text-xs md:text-sm mb-8 text-center">Retrieving evidence and analyzing source reliability...</p>

              <div className="w-full max-w-sm flex flex-col gap-3">
                {scanSteps.map((step, idx) => {
                  let statusClass = 'opacity-40';
                  let itemBorder = 'border-brand-border bg-black/5';
                  let bulletBg = 'border-slate-700 text-slate-500';
                  let iconColor = 'text-slate-500';

                  if (currentStep > idx) {
                    statusClass = 'opacity-85';
                    itemBorder = 'border-brand-true/10 bg-brand-true/[0.01]';
                    bulletBg = 'border-brand-true bg-brand-true text-white';
                    iconColor = 'text-brand-true';
                  } else if (currentStep === idx) {
                    statusClass = 'opacity-100';
                    itemBorder = 'border-brand-primary/30 bg-brand-primary/[0.03]';
                    bulletBg = 'border-brand-primary text-brand-primary animate-pulse-glow';
                    iconColor = 'text-brand-secondary';
                  }

                  return (
                    <div key={idx} className={`flex items-center gap-3.5 p-3 rounded-lg border transition-all duration-200 ${itemBorder} ${statusClass}`}>
                      <div className={`w-5.5 h-5.5 rounded-full border-2 flex items-center justify-center text-[10px] font-bold flex-shrink-0 transition-all duration-200 ${bulletBg}`}>
                        {currentStep > idx ? '✓' : idx + 1}
                      </div>
                      <div className={`flex items-center ${iconColor}`}>
                        {step.icon}
                      </div>
                      <span className={`text-xs font-semibold ${currentStep === idx ? 'text-white' : 'text-slate-400'}`}>
                        {step.label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          /* VERIFICATION RESULT PANEL */
          <div className="bg-brand-bg-surface border border-brand-border rounded-xl p-6 md:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 pb-4 border-b border-brand-border">
              <div>
                <h1 className="font-sans text-xl font-bold text-white">Verification Integrity Report</h1>
                <p className="text-slate-400 text-xs mt-0.5">
                  Scanned in {result.language && <span>Language: <strong>{result.language.toUpperCase()}</strong> // </span>} Created: <strong>{new Date(result.created_at || Date.now()).toLocaleTimeString()}</strong>
                </p>
              </div>
              <button className="bg-transparent border border-brand-border text-slate-300 px-3 py-1.5 rounded-lg font-sans font-semibold text-xs hover:text-white hover:border-slate-500 flex items-center gap-1.5 transition duration-200 cursor-pointer select-none" onClick={handleReset}>
                <ArrowLeft size={14} /> Scan New Claim
              </button>
            </div>

            {/* Split Pane for Image and OCR Extraction */}
            {tab === 'image' && extractedOcrText && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
                <div className="bg-black/10 border border-brand-border rounded-lg p-4">
                  <div className="font-sans font-bold text-[10px] uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">📸 Verified Image Source</div>
                  <div className="w-full max-h-56 overflow-hidden rounded border border-white/5 flex items-center justify-center bg-black/20">
                    <img src={imagePreview} alt="Scanned screenshot" className="max-w-full max-h-56 object-contain" />
                  </div>
                </div>
                <div className="bg-black/10 border border-brand-border rounded-lg p-4">
                  <div className="font-sans font-bold text-[10px] uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">📝 Extracted OCR Text</div>
                  <div className="font-sans text-xs text-slate-300 h-56 overflow-y-auto pr-2 scrollbar-thin">
                    {extractedOcrText}
                  </div>
                </div>
              </div>
            )}

            <div className="text-base font-medium italic border-l-3 border-brand-primary pl-4 py-2 pr-2 bg-black/10 rounded-r text-slate-200 mb-6">
              " {result.original_text} "
            </div>

            {/* If multiple claims detected inside the query */}
            {result.claims && result.claims.length > 1 && (
              <div className="mb-6">
                <div className="font-sans font-bold text-[10px] uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-2">🔍 Detected Assertions ({result.claims.length})</div>
                <div className="flex flex-col gap-2">
                  {result.claims.map((claimObj, idx) => (
                    <button
                      key={idx}
                      className={`flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 p-3.5 border rounded-lg cursor-pointer hover:bg-black/10 hover:border-slate-500 transition-all duration-200 text-left select-none ${selectedClaimIndex === idx ? 'bg-brand-primary/5 border-brand-primary' : 'border-brand-border bg-black/5'}`}
                      onClick={() => setSelectedClaimIndex(idx)}
                    >
                      <span className="font-semibold text-xs md:text-sm text-slate-200 pr-4">{idx + 1}. {claimObj.claim}</span>
                      <span className={`font-sans font-bold text-xs ${getVerdictTheme(claimObj.verification.verdict).textClass}`}>
                        {getVerdictTheme(claimObj.verification.verdict).label}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Active Claim Analysis Panels */}
            {activeClaim ? (
              <>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-6">
                  {/* Verdict Info Card */}
                  <div className={`lg:col-span-2 flex flex-col p-5 md:p-6 rounded-xl relative min-h-[180px] ${activeVerdict.class}`}>
                    <span className="text-[10px] font-sans font-bold uppercase tracking-wider text-slate-400 mb-1">AI Credibility Verdict</span>
                    <h2 className="font-sans text-2xl font-bold tracking-tight mb-3 flex items-center gap-2.5">
                      {activeVerdict.icon}
                      <span className={activeVerdict.textClass}>{activeVerdict.label}</span>
                    </h2>

                    <p className="text-xs md:text-sm text-slate-300 mb-5 leading-relaxed">
                      {activeClaim.trust_report ? activeClaim.trust_report.summary : activeClaim.verification.reason}
                    </p>

                    <div className="flex flex-wrap gap-x-5 gap-y-2 border-t border-brand-border pt-3 mt-auto">
                      <div className="flex flex-col">
                        <span className="text-[9px] text-slate-500 font-semibold uppercase tracking-wider">Topic Area</span>
                        <span className="font-sans font-bold text-xs text-white mt-0.5">{activeClaim.topic || 'General Information'}</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[9px] text-slate-500 font-semibold uppercase tracking-wider">Evidence Method</span>
                        <span className="font-sans font-bold text-xs text-white mt-0.5">
                          {activeClaim.evidence_source === 'VECTOR_CACHE' ? 'Vector Cache Lookup' : 'Real-time Web Crawler'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Confidence Gauge Circular Card */}
                  <div className="lg:col-span-1 flex flex-col items-center justify-center bg-black/10 border border-brand-border rounded-xl p-5 text-center min-h-[180px]">
                    <div className="relative w-28 h-28 mb-3.5 flex items-center justify-center">
                      <svg className="rotate-[-90deg] w-full h-full" viewBox="0 0 120 120">
                        <circle cx="60" cy="60" r={radius} className="fill-none stroke-white/[0.02] stroke-[5px]" />
                        <circle
                          cx="60"
                          cy="60"
                          r={radius}
                          className="fill-none stroke-[6px] stroke-linecap-round transition-[stroke-dashoffset] duration-1000 ease-out"
                          stroke={activeVerdict.color}
                          strokeDasharray={circumference}
                          strokeDashoffset={strokeDashoffset}
                        />
                      </svg>
                      <div className="absolute font-sans text-xl font-bold text-white flex flex-col items-center">
                        <span>{confidencePercent}%</span>
                        <span className="text-[8px] text-slate-500 font-bold uppercase tracking-wider">Confidence</span>
                      </div>
                    </div>
                    <p className="text-[10px] text-slate-400 max-w-[180px] leading-relaxed">
                      Probability reflecting support strength in source corpus.
                    </p>
                  </div>
                </div>

                {/* Evidence Quote highlighting */}
                {(activeClaim.trust_report?.evidence || activeClaim.verification.evidence_quote) && (
                  <div className="bg-black/5 border border-brand-border rounded-lg p-4 mb-6">
                    <div className="font-sans font-bold text-xs text-white mb-2 flex items-center gap-1.5">
                      <FileText size={16} className="text-brand-warn" /> Primary Evidence Extract
                    </div>
                    <p className="font-sans text-xs md:text-sm italic text-slate-400 border-l-2 border-brand-secondary pl-3.5 py-0.5 leading-relaxed">
                      "{activeClaim.trust_report ? activeClaim.trust_report.evidence : activeClaim.verification.evidence_quote}"
                    </p>
                  </div>
                )}

                {/* Sources list */}
                {activeClaim.sources && activeClaim.sources.length > 0 && (
                  <div>
                    <h3 className="font-sans font-bold text-sm md:text-base text-white mb-3 flex items-center gap-1.5">
                      <Globe size={16} className="text-brand-true" /> Verified Citations & References ({activeClaim.sources.length})
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                      {activeClaim.sources.map((src, idx) => (
                        <div key={idx} className="bg-black/5 border border-brand-border rounded-lg p-4 transition-all duration-200 flex flex-col justify-between hover:border-slate-500 group">
                          <span className={`self-start text-[8px] px-1.5 py-0.5 border rounded-full font-bold uppercase tracking-wider mb-2 bg-brand-secondary/5 border-brand-secondary/10 text-brand-secondary`}>
                            {activeClaim.evidence_source === 'VECTOR_CACHE' ? 'Cached Evidence' : `Source #${idx + 1}`}
                          </span>
                          <h4 className="font-sans font-semibold text-xs md:text-sm text-white mb-3.5 line-clamp-2 leading-snug" title={src.title || src.url}>
                            {src.title || 'Untitled Source Document'}
                          </h4>
                          {src.url && (
                            <a
                              href={src.url}
                              target="_blank"
                              rel="noreferrer"
                              className="mt-auto font-sans text-[10px] font-semibold text-brand-secondary hover:text-cyan-400 flex items-center gap-1 transition-all duration-150 cursor-pointer"
                            >
                              Explore Source Website <ExternalLink size={12} />
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-8">
                <HelpCircle size={40} className="opacity-35 mx-auto mb-2 text-slate-500" />
                <p className="text-slate-400 text-sm">No verification details available for this statement.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
