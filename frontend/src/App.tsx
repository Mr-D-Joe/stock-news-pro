import React from 'react';
import { ErrorBoundary } from './components/ErrorBoundary';
import { AppProvider, useAppContext } from './context/AppContext';
import { TopBar } from '@/components/TopBar';
import { MarketOverviewCard } from '@/components/dashboard/MarketOverviewCard';
import { DashboardHero } from '@/components/dashboard/DashboardHero';
import { EventMonitorCard } from '@/components/dashboard/EventMonitorCard';
import { NewsTicker } from '@/components/dashboard/NewsTicker';
import { SummarizerCard } from '@/components/dashboard/SummarizerCard';
import { EssayCard } from '@/components/dashboard/EssayCard';
import { StatusBar } from '@/components/StatusBar';
import { Activity } from 'lucide-react';

import { HeatmapCard } from '@/components/dashboard/HeatmapCard';
import { WatchlistCard } from '@/components/dashboard/WatchlistCard';
import { BackendService } from '@/services/BackendService';

const Dashboard = () => {
  const { uiState, analysisStatus, analysisResult } = useAppContext();
  const [backendReady, setBackendReady] = React.useState<boolean>(false);

  // Initialize Backend on Mount
  React.useEffect(() => {
    const initBackend = async () => {
      const healthy = await BackendService.init();
      setBackendReady(healthy);
      if (!healthy) {
        // In DEV_MODE we might just log warning, or show error if critical
        console.warn("Backend unavailable - proceeding in potential Mock-Only mode manually?");
      }
    };
    initBackend();
  }, []);
  const { selectedSector } = uiState;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900 overflow-hidden">

      {/* 1. SECTOR & STOCK NEWS TICKERS (STACKED) */}
      {analysisResult && (
        <div className="flex flex-col border-b border-slate-800">
          {/* Upper: Sector News */}
          <div className="bg-slate-900 text-slate-200">
            <NewsTicker
              news={analysisResult.sectorNews}
              label={`${selectedSector} NEWS`}
            />
          </div>
          {/* Lower: Stock News */}
          <div className="bg-slate-800 text-white border-t border-slate-700">
            <NewsTicker
              news={analysisResult.stockNews}
              label={`${analysisResult.report.stock} NEWS`}
            />
          </div>
        </div>
      )}

      {/* 2. TOP BAR */}
      <TopBar />

      {/* 3. MAIN DASHBOARD CONTENT */}
      <main className="flex-1 overflow-y-auto p-6 md:p-8 custom-scrollbar">
        <div className="max-w-[1800px] mx-auto min-h-full">

          {/* IDLE STATE - HERO VIEW */}
          {analysisStatus === 'idle' && !analysisResult && (
            <DashboardHero />
          )}

          {/* STRICT 2-COL LAYOUT */}
          {analysisResult && (
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">

              {/* --- LEFT COLUMN: MARKET OVERVIEW (40-45%) --- */}
              <div className="xl:col-span-5 space-y-6">
                <MarketOverviewCard
                  executiveSummary={analysisResult.report.summary}
                  reviewData={analysisResult.report.reviewData}
                  analystRatings={analysisResult.report.analystRatings}
                  riskAssessment={analysisResult.report.riskAssessment}
                  marketSentiment={analysisResult.report.marketSentiment}
                  businessContext={analysisResult.report.businessContext}
                  generatedAt={analysisResult.report.generatedAt}
                />
              </div>

              {/* --- RIGHT COLUMN: EVENT & AI MONITOR (55-60%) --- */}
              <div className="xl:col-span-7 space-y-6">



                {/* B. PRICE CHART & MONITOR */}
                <EventMonitorCard
                  chartData={analysisResult.chartData}
                  volumeData={analysisResult.volumeData}
                  selectedPeriod="1Y"
                  sectorNews={analysisResult.sectorNews.map((n: { title: string }) => n.title).slice(0, 5)}
                />

                {/* C. AI OUTPUTS STACKED */}
                <div className="grid grid-cols-1 gap-6">
                  <SummarizerCard
                    summary={analysisResult.report.deepAnalysis}
                    metrics={[]}
                  />
                  <EssayCard text={analysisResult.essay} />
                </div>
              </div>

            </div>
          )}
        </div>
      </main>

      <StatusBar
        statusMessage={
          !backendReady
            ? "System Alert • Backend Unavailable (Mock Mode)"
            : analysisStatus === 'loading'
              ? "Processing Real-Time Data Stream..."
              : "System Operational • Backend Connected"
        }
        versionInfo="v1.5.0-desktop"
      />
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <ErrorBoundary>
        <Dashboard />
      </ErrorBoundary>
    </AppProvider>
  );
}

export default App;
